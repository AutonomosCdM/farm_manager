import sys
import os
import json
import pytest
from datetime import datetime, timedelta
from dataclasses import dataclass

sys.path.insert(0, '/Users/autonomos_dev/Projects/gantt_nuts')
from src.resource_management import ResourceManager, ResourceOptimizer, Machinery

# Define a Task class for testing
@dataclass
class Task:
    id: str
    name: str
    type: str
    priority: int
    location: str

# Test fixtures
@pytest.fixture
def resource_manager():
    """Create a test resource manager with test data directory."""
    test_data_dir = "test_resource_data"
    
    # Clean up any existing test data
    if os.path.exists(test_data_dir):
        if os.path.exists(os.path.join(test_data_dir, "machinery.json")):
            os.remove(os.path.join(test_data_dir, "machinery.json"))
        if os.path.exists(os.path.join(test_data_dir, "personnel.json")):
            os.remove(os.path.join(test_data_dir, "personnel.json"))
        if os.path.exists(os.path.join(test_data_dir, "usage_log.json")):
            os.remove(os.path.join(test_data_dir, "usage_log.json"))
    else:
        os.makedirs(test_data_dir)
    
    # Create resource manager with test data directory
    rm = ResourceManager(data_dir=test_data_dir)
    
    # Add test machinery
    rm.register_machinery(
        name="Test Tractor 1",
        type="Tractor",
        status="available",
        last_maintenance_date=datetime.now().isoformat(),
        purchase_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    )
    
    rm.register_machinery(
        name="Test Tractor 2",
        type="Tractor",
        status="available",
        last_maintenance_date=None,
        purchase_date=(datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
    )
    
    rm.register_machinery(
        name="Test Harvester",
        type="Harvester",
        status="available",
        last_maintenance_date=datetime.now().isoformat(),
        purchase_date=(datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    )
    
    rm.register_machinery(
        name="Test Sprayer",
        type="Sprayer",
        status="available",
        last_maintenance_date=None,
        purchase_date=(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    )
    
    yield rm
    
    # Clean up test data
    if os.path.exists(test_data_dir):
        if os.path.exists(os.path.join(test_data_dir, "machinery.json")):
            os.remove(os.path.join(test_data_dir, "machinery.json"))
        if os.path.exists(os.path.join(test_data_dir, "personnel.json")):
            os.remove(os.path.join(test_data_dir, "personnel.json"))
        if os.path.exists(os.path.join(test_data_dir, "usage_log.json")):
            os.remove(os.path.join(test_data_dir, "usage_log.json"))

@pytest.fixture
def test_tasks():
    """Create test tasks for optimization testing."""
    return [
        Task(id="task1", name="Plowing Field A", type="Tractor", priority=3, location="Field A"),
        Task(id="task2", name="Harvesting Field B", type="Harvester", priority=2, location="Field B"),
        Task(id="task3", name="Spraying Field C", type="Sprayer", priority=1, location="Field C"),
        Task(id="task4", name="Plowing Field D", type="Tractor", priority=4, location="Field D")
    ]

# Tests for machinery efficiency calculation
def test_machinery_efficiency_calculation(resource_manager):
    """Test the calculation of machinery efficiency based on various factors."""
    # Get test machinery
    machinery = resource_manager.get_all_machinery()
    
    # Create test tasks
    tractor_task = Task(id="task1", name="Plowing", type="Tractor", priority=1, location="Field A")
    harvester_task = Task(id="task2", name="Harvesting", type="Harvester", priority=1, location="Field B")
    
    # Test efficiency calculation for each machine with matching task
    for machine in machinery:
        task = tractor_task if machine.type == "Tractor" else harvester_task
        efficiency = ResourceOptimizer.calculate_machinery_efficiency(machine, task)
        
        # Efficiency should be higher for:
        # 1. Machines with matching type
        # 2. Machines with recent maintenance
        # 3. Available machines
        # 4. Newer machines
        
        # Basic check: efficiency should be a number
        assert isinstance(efficiency, (int, float))
        
        # Type matching should increase efficiency
        if machine.type == task.type:
            assert efficiency >= 1.0
        
        # Maintenance should increase efficiency
        if machine.last_maintenance_date:
            # Compare with a similar machine without maintenance
            similar_machines = [m for m in machinery if m.type == machine.type and not m.last_maintenance_date]
            if similar_machines:
                similar_efficiency = ResourceOptimizer.calculate_machinery_efficiency(similar_machines[0], task)
                assert efficiency > similar_efficiency

# Tests for machinery assignment optimization
def test_machinery_assignment_optimization(resource_manager, test_tasks):
    """Test the optimization of machinery assignments based on task priorities and machine efficiency."""
    # Get assignments
    assignments = ResourceOptimizer.optimize_machinery_assignment(resource_manager, test_tasks)
    
    # Check that assignments were made
    assert len(assignments) > 0
    
    # Check that high priority tasks were assigned
    high_priority_tasks = sorted(test_tasks, key=lambda t: t.priority, reverse=True)[:2]
    for task in high_priority_tasks:
        assert task.id in assignments
    
    # Check that assignments match task types
    for task_id, machine_id in assignments.items():
        task = next(t for t in test_tasks if t.id == task_id)
        machine = resource_manager.get_machinery(machine_id)
        
        # Ideally, machine type should match task type
        # But if not enough machines of the right type, this might not always be true
        if sum(1 for t in test_tasks if t.type == task.type) <= sum(1 for m in resource_manager.get_all_machinery() if m.type == task.type):
            assert machine.type == task.type

# Tests for conflict resolution
def test_assignment_conflict_resolution(resource_manager):
    """Test the resolution of conflicts in machinery assignments."""
    # Create conflicting tasks (same type, different priorities)
    tasks = [
        Task(id="task1", name="High Priority Plowing", type="Tractor", priority=3, location="Field A"),
        Task(id="task2", name="Medium Priority Plowing", type="Tractor", priority=2, location="Field B"),
        Task(id="task3", name="Low Priority Plowing", type="Tractor", priority=1, location="Field C")
    ]
    
    # Get all tractors
    tractors = resource_manager.get_machinery_by_type("Tractor")
    
    # Create conflicting assignments (multiple tasks assigned to same machine)
    assignments = {
        "task1": tractors[0].id,
        "task2": tractors[0].id,  # Conflict with task1
        "task3": tractors[1].id
    }
    
    # Define priorities
    priorities = {
        "task1": 3,
        "task2": 2,
        "task3": 1
    }
    
    # Resolve conflicts
    resolved = ResourceOptimizer.resolve_assignment_conflicts(
        resource_manager, assignments, priorities
    )
    
    # Check that conflicts were resolved
    machine_to_tasks = {}
    for task_id, machine_id in resolved.items():
        if machine_id not in machine_to_tasks:
            machine_to_tasks[machine_id] = []
        machine_to_tasks[machine_id].append(task_id)
    
    # Each machine should have at most one task
    for machine_id, task_ids in machine_to_tasks.items():
        assert len(task_ids) == 1
    
    # High priority tasks should be kept
    assert "task1" in resolved
    assert "task3" in resolved
    
    # Lower priority conflicting task should be removed
    assert "task2" not in resolved
