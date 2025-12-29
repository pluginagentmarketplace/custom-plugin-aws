#!/usr/bin/env python3
"""
API Validator
Validates OpenAPI specs and API responses.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urlparse


class APIValidator:
    """Validate OpenAPI specifications and API responses."""

    def __init__(self, spec_path: str = None):
        self.spec = None
        if spec_path:
            self.load_spec(spec_path)

    def load_spec(self, path: str) -> Dict:
        """Load OpenAPI specification from file."""
        spec_path = Path(path)
        with open(spec_path) as f:
            if spec_path.suffix in ['.yaml', '.yml']:
                self.spec = yaml.safe_load(f)
            else:
                self.spec = json.load(f)
        return self.spec

    def validate_spec(self) -> Dict[str, List[str]]:
        """Validate OpenAPI specification structure."""
        if not self.spec:
            return {"errors": ["No specification loaded"]}

        errors = []
        warnings = []

        # Check required fields
        if 'openapi' not in self.spec:
            errors.append("Missing 'openapi' version field")

        if 'info' not in self.spec:
            errors.append("Missing 'info' section")
        else:
            if 'title' not in self.spec['info']:
                errors.append("Missing 'info.title'")
            if 'version' not in self.spec['info']:
                errors.append("Missing 'info.version'")

        if 'paths' not in self.spec:
            errors.append("Missing 'paths' section")

        # Validate paths
        for path, methods in self.spec.get('paths', {}).items():
            if not path.startswith('/'):
                errors.append(f"Path '{path}' must start with '/'")

            for method, operation in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head', 'parameters']:
                    continue

                if 'responses' not in operation:
                    errors.append(f"Missing 'responses' in {method.upper()} {path}")

                if 'operationId' not in operation:
                    warnings.append(f"Missing 'operationId' in {method.upper()} {path}")

        # Validate components
        components = self.spec.get('components', {})
        schemas = components.get('schemas', {})

        for name, schema in schemas.items():
            if 'type' not in schema and '$ref' not in schema and 'oneOf' not in schema:
                warnings.append(f"Schema '{name}' missing 'type' definition")

        return {"errors": errors, "warnings": warnings}

    def validate_response(self, path: str, method: str,
                         status_code: int, response: Dict) -> Dict:
        """Validate API response against specification."""
        if not self.spec:
            return {"valid": False, "errors": ["No specification loaded"]}

        errors = []

        # Get operation
        path_spec = self.spec.get('paths', {}).get(path)
        if not path_spec:
            return {"valid": False, "errors": [f"Path '{path}' not found in spec"]}

        operation = path_spec.get(method.lower())
        if not operation:
            return {"valid": False, "errors": [f"Method '{method}' not found for path '{path}'"]}

        # Get response spec
        responses = operation.get('responses', {})
        response_spec = responses.get(str(status_code)) or responses.get('default')

        if not response_spec:
            return {"valid": False, "errors": [f"Status {status_code} not defined for {method.upper()} {path}"]}

        # Get schema
        content = response_spec.get('content', {})
        json_content = content.get('application/json', {})
        schema = json_content.get('schema')

        if schema:
            schema_errors = self._validate_against_schema(response, schema)
            errors.extend(schema_errors)

        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_against_schema(self, data: Any, schema: Dict,
                                 path: str = "") -> List[str]:
        """Validate data against JSON schema."""
        errors = []

        # Handle $ref
        if '$ref' in schema:
            ref_path = schema['$ref'].split('/')
            ref_schema = self.spec
            for part in ref_path[1:]:
                ref_schema = ref_schema.get(part, {})
            return self._validate_against_schema(data, ref_schema, path)

        schema_type = schema.get('type')

        # Type validation
        if schema_type == 'object':
            if not isinstance(data, dict):
                errors.append(f"{path}: Expected object, got {type(data).__name__}")
                return errors

            # Required fields
            required = schema.get('required', [])
            for field in required:
                if field not in data:
                    errors.append(f"{path}.{field}: Required field missing")

            # Validate properties
            properties = schema.get('properties', {})
            for prop, prop_schema in properties.items():
                if prop in data:
                    errors.extend(self._validate_against_schema(
                        data[prop], prop_schema, f"{path}.{prop}"
                    ))

        elif schema_type == 'array':
            if not isinstance(data, list):
                errors.append(f"{path}: Expected array, got {type(data).__name__}")
                return errors

            items_schema = schema.get('items', {})
            for i, item in enumerate(data):
                errors.extend(self._validate_against_schema(
                    item, items_schema, f"{path}[{i}]"
                ))

        elif schema_type == 'string':
            if not isinstance(data, str):
                errors.append(f"{path}: Expected string, got {type(data).__name__}")

        elif schema_type == 'integer':
            if not isinstance(data, int) or isinstance(data, bool):
                errors.append(f"{path}: Expected integer, got {type(data).__name__}")

        elif schema_type == 'number':
            if not isinstance(data, (int, float)) or isinstance(data, bool):
                errors.append(f"{path}: Expected number, got {type(data).__name__}")

        elif schema_type == 'boolean':
            if not isinstance(data, bool):
                errors.append(f"{path}: Expected boolean, got {type(data).__name__}")

        return errors

    def generate_mock_response(self, path: str, method: str,
                               status_code: int = 200) -> Dict:
        """Generate mock response based on schema."""
        if not self.spec:
            return {}

        operation = self.spec.get('paths', {}).get(path, {}).get(method.lower(), {})
        response_spec = operation.get('responses', {}).get(str(status_code), {})
        content = response_spec.get('content', {}).get('application/json', {})
        schema = content.get('schema', {})

        return self._generate_from_schema(schema)

    def _generate_from_schema(self, schema: Dict) -> Any:
        """Generate mock data from schema."""
        if '$ref' in schema:
            ref_path = schema['$ref'].split('/')
            ref_schema = self.spec
            for part in ref_path[1:]:
                ref_schema = ref_schema.get(part, {})
            return self._generate_from_schema(ref_schema)

        schema_type = schema.get('type')

        if schema_type == 'object':
            result = {}
            for prop, prop_schema in schema.get('properties', {}).items():
                result[prop] = self._generate_from_schema(prop_schema)
            return result

        elif schema_type == 'array':
            items_schema = schema.get('items', {})
            return [self._generate_from_schema(items_schema)]

        elif schema_type == 'string':
            format_type = schema.get('format')
            if format_type == 'email':
                return "user@example.com"
            elif format_type == 'uuid':
                return "550e8400-e29b-41d4-a716-446655440000"
            elif format_type == 'date-time':
                return "2024-01-15T10:30:00Z"
            return "string"

        elif schema_type == 'integer':
            return 0

        elif schema_type == 'number':
            return 0.0

        elif schema_type == 'boolean':
            return True

        return None


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="API Validator")
    parser.add_argument("spec", help="OpenAPI spec file")
    parser.add_argument("--validate", action="store_true", help="Validate spec")
    parser.add_argument("--mock", nargs=2, metavar=("PATH", "METHOD"),
                        help="Generate mock response")

    args = parser.parse_args()

    validator = APIValidator(args.spec)

    if args.validate:
        result = validator.validate_spec()
        print(json.dumps(result, indent=2))

    elif args.mock:
        mock = validator.generate_mock_response(args.mock[0], args.mock[1])
        print(json.dumps(mock, indent=2))


if __name__ == "__main__":
    main()
