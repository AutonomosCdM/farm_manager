#!/usr/bin/env python
"""
Machinery Optimization Demo

This script demonstrates the functionality of the ResourceManager and ResourceOptimizer
classes for agricultural machinery management and optimization.
"""

import sys
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List

from src.resource_management import ResourceManager, ResourceOptimizer, Machinery

# Define a Task class for demonstration
@dataclass
class Task:
    id: str
    name: str
    type: str
    priority: int
    location: str

def print_separator():
    """Print a separator line for better readability."""
    print("\n" + "=" * 80 + "\n")

def main():
    """Main demonstration function."""
    print("Agricultural Machinery Optimization System Demo")
    print_separator()
    
    # Create a resource manager
    print("Initializing Resource Manager...")
    rm = ResourceManager()
    
    # Register machinery
    print("Registering machinery...")
    tractors = []
    for i in range(3):
        tractor = rm.register_machinery(
            name=f"John Deere 6110M #{i+1}",
            type="Tractor",
            status="available",
            last_maintenance_date=datetime.now().isoformat() if i == 0 else None,
            purchase_date=(datetime.now() - timedelta(days=365 * (i+1))).strftime('%Y-%m-%d')
        )
        tractors.append(tractor)
        print(f"  Registered: {tractor.name} (ID: {tractor.id})")
    
    harvester = rm.register_machinery(
        name="New Holland CR9.90",
        type="Harvester",
        status="available",
        last_maintenance_date=datetime.now().isoformat(),
        purchase_date=(datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    )
    print(f"  Registered: {harvester.name} (ID: {harvester.id})")
    
    sprayer = rm.register_machinery(
        name="Hardi Commander",
        type="Sprayer",
        status="available",
        last_maintenance_date=None,
        purchase_date=(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    )
    print(f"  Registered: {sprayer.name} (ID: {sprayer.id})")
    
    print_separator()
    
    # Create tasks
    print("Creating agricultural tasks...")
    tasks = [
        Task(id="task1", name="Plowing Field A", type="Tractor", priority=3, location="Field A"),
        Task(id="task2", name="Harvesting Field B", type="Harvester", priority=2, location="Field B"),
        Task(id="task3", name="Spraying Field C", type="Sprayer", priority=1, location="Field C"),
        Task(id="task4", name="Plowing Field D", type="Tractor", priority=4, location="Field D"),
        Task(id="task5", name="Plowing Field E", type="Tractor", priority=2, location="Field E")
    ]
    
    for task in tasks:
        print(f"  Task: {task.name} (Priority: {task.priority}, Type: {task.type})")
    
    print_separator()
    
    # Calculate efficiency for each machine with a tractor task
    print("Calculating machinery efficiency for tractor tasks...")
    tractor_task = tasks[0]  # A tractor task
    
    # Only use the machines we just created for the demo
    demo_machines = tractors + [harvester, sprayer]
    
    for machine in demo_machines:
        efficiency = ResourceOptimizer.calculate_machinery_efficiency(machine, tractor_task)
        print(f"  {machine.name} (Type: {machine.type}): Efficiency = {efficiency:.2f}")
        
        # Explain factors affecting efficiency
        factors = []
        if machine.type == tractor_task.type:
            factors.append("Type match (+2.0)")
        else:
            factors.append("Type mismatch (-1.0)")
            
        if machine.last_maintenance_date:
            factors.append("Recent maintenance (+0.5)")
            
        if machine.status == 'available':
            factors.append("Available status (+0.5)")
            
        if machine.purchase_date:
            age_years = (datetime.now() - datetime.strptime(machine.purchase_date, '%Y-%m-%d')).days / 365
            factors.append(f"Age penalty (-{min(age_years, 1.0):.2f})")
            
        print(f"    Factors: {', '.join(factors)}")
    
    print_separator()
    
    # Create a custom ResourceManager with only our demo machines
    print("Optimizing machinery assignment based on task priorities and machine efficiency...")
    
    # Create a temporary ResourceManager for the demo
    demo_rm = ResourceManager(data_dir="demo_resource_data")
    
    # Add our demo machines to the temporary ResourceManager
    demo_machines_dict = {}
    for machine in demo_machines:
        demo_machines_dict[machine.id] = machine
        demo_rm._save_machinery(demo_machines_dict)
    
    # Optimize using only our demo machines
    assignments = ResourceOptimizer.optimize_machinery_assignment(demo_rm, tasks)
    
    for task_id, machine_id in assignments.items():
        task = next(t for t in tasks if t.id == task_id)
        machine = demo_rm.get_machinery(machine_id)
        print(f"  Task: {task.name} (Priority: {task.priority}) → Machine: {machine.name} (Type: {machine.type})")
    
    # Clean up temporary directory
    import shutil
    if os.path.exists("demo_resource_data"):
        shutil.rmtree("demo_resource_data")
    
    print_separator()
    
    # Create conflicting assignments
    print("Demonstrating conflict resolution...")
    print("Scenario: Multiple high-priority tasks need the same type of machinery")
    
    # Create a temporary ResourceManager for the demo
    demo_rm = ResourceManager(data_dir="demo_resource_data")
    
    # Add our demo machines to the temporary ResourceManager
    demo_machines_dict = {}
    for machine in demo_machines:
        demo_machines_dict[machine.id] = machine
    demo_rm._save_machinery(demo_machines_dict)
    
    # Create conflicting assignments (multiple tasks assigned to same machine)
    # Use the first tractor for two tasks, and the second tractor for one task
    conflicting_assignments = {
        "task1": tractors[0].id,  # Plowing Field A (Priority 3)
        "task4": tractors[0].id,  # Plowing Field D (Priority 4) - Conflict with task1
        "task5": tractors[1].id   # Plowing Field E (Priority 2)
    }
    
    print("Conflicting assignments:")
    for task_id, machine_id in conflicting_assignments.items():
        task = next(t for t in tasks if t.id == task_id)
        machine = next(m for m in demo_machines if m.id == machine_id)
        print(f"  Task: {task.name} (Priority: {task.priority}) → Machine: {machine.name}")
    
    # Define priorities
    priorities = {task.id: task.priority for task in tasks}
    
    # Resolve conflicts
    resolved = ResourceOptimizer.resolve_assignment_conflicts(
        demo_rm, conflicting_assignments, priorities
    )
    
    print("\nResolved assignments (after conflict resolution):")
    for task_id, machine_id in resolved.items():
        task = next(t for t in tasks if t.id == task_id)
        machine = next(m for m in demo_machines if m.id == machine_id)
        print(f"  Task: {task.name} (Priority: {task.priority}) → Machine: {machine.name}")
    
    # Clean up temporary directory
    import shutil
    if os.path.exists("demo_resource_data"):
        shutil.rmtree("demo_resource_data")
    
    print_separator()
    
    # Generate resource report for demo machines only
    print("Generating resource report for demo machines...")
    
    # Create a temporary ResourceManager for the demo
    demo_rm = ResourceManager(data_dir="demo_resource_data")
    
    # Add our demo machines to the temporary ResourceManager
    demo_machines_dict = {}
    for machine in demo_machines:
        demo_machines_dict[machine.id] = machine
    demo_rm._save_machinery(demo_machines_dict)
    
    # Generate report
    report = demo_rm.generate_resource_report()
    
    print("Machinery:")
    print(f"  Total: {report['machinery']['total']}")
    print(f"  Available: {report['machinery']['available']}")
    print(f"  In Use: {report['machinery']['in_use']}")
    print("  By Type:")
    for type_name, count in report['machinery']['by_type'].items():
        print(f"    {type_name}: {count}")
    
    print("\nPersonnel:")
    print(f"  Total: {report['personnel']['total']}")
    print(f"  Available: {report['personnel']['available']}")
    print(f"  Assigned: {report['personnel']['assigned']}")
    
    # Clean up temporary directory
    import shutil
    if os.path.exists("demo_resource_data"):
        shutil.rmtree("demo_resource_data")
    
    print_separator()
    print("Demo completed successfully!")

if __name__ == "__main__":
    main()
