from datetime import datetime
from typing import List, Dict, Any, Optional

from .models import Machinery
from .manager import ResourceManager


class ResourceOptimizer:
    """Class for optimizing resource allocation."""

    @staticmethod
    def calculate_machinery_efficiency(machine: Machinery, task: Any) -> float:
        """Calculate efficiency based on machine type, maintenance history, current status, and age."""
        # Base efficiency
        efficiency = 0

        # Type matching is most important - add a significant bonus
        if machine.type == task.type:
            efficiency += 2.0
        else:
            # If types don't match, efficiency is very low
            efficiency -= 1.0

        # Maintenance history bonus
        if machine.last_maintenance_date:
            efficiency += 0.5

        # Status bonus
        if machine.status == "available":
            efficiency += 0.5

        # Age penalty (newer machines are more efficient)
        if machine.purchase_date:
            try:
                age_years = (
                    datetime.now() - datetime.strptime(machine.purchase_date, "%Y-%m-%d")
                ).days / 365
                # Cap the age penalty to avoid extreme negative values
                age_penalty = min(age_years, 1.0)
                efficiency -= age_penalty
            except ValueError:
                # If date parsing fails, skip age penalty
                pass

        return efficiency

    @staticmethod
    def optimize_machinery_assignment(
        resource_manager: ResourceManager, tasks: List[Any]
    ) -> Dict[str, str]:
        """
        Optimize machinery assignment based on task priority and machinery efficiency.

        Args:
            resource_manager (ResourceManager): The resource management system
            tasks (List[Any]): List of tasks to assign machinery to

        Returns:
            Dict[str, str]: A mapping of task IDs to machinery IDs
        """
        # Get available machinery
        available_machinery = [
            m for m in resource_manager.get_all_machinery() if m.status == "available"
        ]

        # Sort tasks by priority (assuming tasks have a priority attribute)
        sorted_tasks = sorted(tasks, key=lambda t: getattr(t, "priority", 0), reverse=True)

        assignments = {}

        for task in sorted_tasks:
            if not available_machinery:
                break

            # Find machines of matching type
            matching_machines = [m for m in available_machinery if m.type == task.type]

            # If no matching machines, use all available
            machines_to_consider = matching_machines if matching_machines else available_machinery

            if machines_to_consider:
                # Calculate efficiencies
                efficiencies = [
                    (
                        machine,
                        ResourceOptimizer.calculate_machinery_efficiency(machine, task),
                    )
                    for machine in machines_to_consider
                ]

                # Sort by efficiency
                efficiencies.sort(key=lambda x: x[1], reverse=True)

                # Assign most efficient machine
                best_machine, _ = efficiencies[0]
                assignments[task.id] = best_machine.id

                # Remove assigned machine from available list
                available_machinery = [m for m in available_machinery if m.id != best_machine.id]

        return assignments

    @staticmethod
    def resolve_assignment_conflicts(
        resource_manager: ResourceManager,
        assignments: Dict[str, str],
        priorities: Dict[str, int],
    ) -> Dict[str, str]:
        """
        Resolve conflicts in resource assignments based on task priorities.

        Args:
            resource_manager (ResourceManager): The resource management system
            assignments (Dict[str, str]): Current task to machinery assignments
            priorities (Dict[str, int]): Task priorities

        Returns:
            Dict[str, str]: Resolved assignments with conflicts removed
        """
        # Find machines assigned to multiple tasks
        machine_to_tasks = {}
        for task_id, machine_id in assignments.items():
            if machine_id not in machine_to_tasks:
                machine_to_tasks[machine_id] = []
            machine_to_tasks[machine_id].append(task_id)

        # Resolve conflicts
        resolved_assignments = assignments.copy()
        for machine_id, task_ids in machine_to_tasks.items():
            if len(task_ids) > 1:
                # Sort tasks by priority
                sorted_tasks = sorted(task_ids, key=lambda t: priorities.get(t, 0), reverse=True)

                # Keep assignment for highest priority task
                highest_priority_task = sorted_tasks[0]

                # Remove assignments for lower priority tasks
                for task_id in sorted_tasks[1:]:
                    resolved_assignments.pop(task_id)

        return resolved_assignments
