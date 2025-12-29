#!/usr/bin/env python3
"""
Capacity Calculator
Estimate system capacity and infrastructure requirements.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class TrafficEstimate:
    """Traffic estimation parameters."""
    daily_active_users: int
    requests_per_user_per_day: int
    peak_multiplier: float = 3.0
    read_write_ratio: float = 0.8  # 80% reads


@dataclass
class StorageEstimate:
    """Storage estimation parameters."""
    data_per_user_mb: float
    growth_rate_monthly: float = 0.1
    retention_years: int = 3


class CapacityCalculator:
    """Calculate infrastructure capacity requirements."""

    def calculate_traffic(self, estimate: TrafficEstimate) -> Dict:
        """Calculate traffic metrics."""
        daily_requests = estimate.daily_active_users * estimate.requests_per_user_per_day
        requests_per_second = daily_requests / 86400
        peak_rps = requests_per_second * estimate.peak_multiplier

        read_rps = peak_rps * estimate.read_write_ratio
        write_rps = peak_rps * (1 - estimate.read_write_ratio)

        return {
            "daily_requests": daily_requests,
            "average_rps": round(requests_per_second, 2),
            "peak_rps": round(peak_rps, 2),
            "read_rps": round(read_rps, 2),
            "write_rps": round(write_rps, 2)
        }

    def calculate_storage(self, users: int, estimate: StorageEstimate) -> Dict:
        """Calculate storage requirements."""
        current_storage_gb = (users * estimate.data_per_user_mb) / 1024
        monthly_growth_gb = current_storage_gb * estimate.growth_rate_monthly
        year_1_storage = current_storage_gb * (1 + estimate.growth_rate_monthly) ** 12
        year_3_storage = current_storage_gb * (1 + estimate.growth_rate_monthly) ** 36

        return {
            "current_storage_gb": round(current_storage_gb, 2),
            "monthly_growth_gb": round(monthly_growth_gb, 2),
            "year_1_storage_gb": round(year_1_storage, 2),
            "year_3_storage_gb": round(year_3_storage, 2)
        }

    def calculate_bandwidth(self, traffic: Dict, avg_response_kb: float) -> Dict:
        """Calculate bandwidth requirements."""
        peak_bandwidth_mbps = (traffic["peak_rps"] * avg_response_kb * 8) / 1024
        daily_transfer_gb = (traffic["daily_requests"] * avg_response_kb) / (1024 * 1024)
        monthly_transfer_gb = daily_transfer_gb * 30

        return {
            "peak_bandwidth_mbps": round(peak_bandwidth_mbps, 2),
            "daily_transfer_gb": round(daily_transfer_gb, 2),
            "monthly_transfer_gb": round(monthly_transfer_gb, 2)
        }

    def calculate_instances(self, traffic: Dict,
                           requests_per_instance: int = 1000) -> Dict:
        """Calculate instance requirements."""
        min_instances = max(2, int(traffic["average_rps"] / requests_per_instance) + 1)
        peak_instances = int(traffic["peak_rps"] / requests_per_instance) + 1

        return {
            "min_instances": min_instances,
            "peak_instances": peak_instances,
            "recommended_instances": max(min_instances, int(peak_instances * 0.7))
        }

    def calculate_database(self, traffic: Dict, storage: Dict) -> Dict:
        """Calculate database requirements."""
        connections_needed = int(traffic["peak_rps"] * 0.1)  # 10% connection ratio
        iops_needed = int(traffic["write_rps"] * 2 + traffic["read_rps"] * 0.5)

        # Instance sizing
        if traffic["peak_rps"] < 1000:
            instance_class = "db.t3.medium"
        elif traffic["peak_rps"] < 5000:
            instance_class = "db.r6g.large"
        elif traffic["peak_rps"] < 20000:
            instance_class = "db.r6g.xlarge"
        else:
            instance_class = "db.r6g.2xlarge"

        return {
            "recommended_instance": instance_class,
            "storage_gb": int(storage["year_1_storage_gb"] * 1.5),
            "iops": iops_needed,
            "max_connections": max(100, connections_needed),
            "read_replicas": 1 if traffic["read_rps"] > 1000 else 0
        }

    def calculate_cache(self, traffic: Dict, cache_hit_rate: float = 0.8) -> Dict:
        """Calculate cache requirements."""
        cached_requests = traffic["read_rps"] * cache_hit_rate
        memory_per_key_kb = 2
        estimated_keys = int(traffic["daily_requests"] * 0.01)  # 1% unique cached
        memory_needed_gb = (estimated_keys * memory_per_key_kb) / (1024 * 1024)

        if memory_needed_gb < 1:
            node_type = "cache.t3.micro"
        elif memory_needed_gb < 6:
            node_type = "cache.r6g.large"
        else:
            node_type = "cache.r6g.xlarge"

        return {
            "cached_rps": round(cached_requests, 2),
            "estimated_keys": estimated_keys,
            "memory_needed_gb": round(memory_needed_gb, 2),
            "recommended_node": node_type,
            "num_nodes": 2 if traffic["peak_rps"] > 5000 else 1
        }

    def full_estimate(self, users: int, requests_per_user: int = 50,
                     data_per_user_mb: float = 10) -> Dict:
        """Generate full infrastructure estimate."""
        traffic_estimate = TrafficEstimate(
            daily_active_users=users,
            requests_per_user_per_day=requests_per_user
        )
        storage_estimate = StorageEstimate(data_per_user_mb=data_per_user_mb)

        traffic = self.calculate_traffic(traffic_estimate)
        storage = self.calculate_storage(users, storage_estimate)
        bandwidth = self.calculate_bandwidth(traffic, avg_response_kb=50)
        instances = self.calculate_instances(traffic)
        database = self.calculate_database(traffic, storage)
        cache = self.calculate_cache(traffic)

        return {
            "users": users,
            "traffic": traffic,
            "storage": storage,
            "bandwidth": bandwidth,
            "compute": instances,
            "database": database,
            "cache": cache
        }


def main():
    """Example usage."""
    import json

    calculator = CapacityCalculator()

    # Example: 100K daily active users
    estimate = calculator.full_estimate(
        users=100000,
        requests_per_user=50,
        data_per_user_mb=10
    )

    print("Infrastructure Capacity Estimate")
    print("=" * 50)
    print(json.dumps(estimate, indent=2))


if __name__ == "__main__":
    main()
