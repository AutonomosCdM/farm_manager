import json
import uuid
import os
from datetime import datetime
from typing import List, Dict, Optional, Any, Union

class Machinery:
    """Class representing agricultural machinery resources."""
    
    def __init__(self, name: str, type: str, status: str = "available", 
                 last_maintenance_date: Optional[str] = None, 
                 purchase_date: Optional[str] = None, id: Optional[str] = None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.type = type
        self.status = status
        self.last_maintenance_date = last_maintenance_date
        self.purchase_date = purchase_date
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert machinery object to dictionary for serialization."""
        return {
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "last_maintenance_date": self.last_maintenance_date,
            "purchase_date": self.purchase_date
        }
    
    @classmethod
    def from_dict(cls, id: str, data: Dict[str, Any]) -> 'Machinery':
        """Create machinery object from dictionary."""
        return cls(
            id=id,
            name=data["name"],
            type=data["type"],
            status=data["status"],
            last_maintenance_date=data.get("last_maintenance_date"),
            purchase_date=data.get("purchase_date")
        )


class Personnel:
    """Class representing agricultural personnel resources."""
    
    def __init__(self, name: str, role: str, department: str, 
                 status: str = "available", skills: List[str] = None, 
                 id: Optional[str] = None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.role = role
        self.department = department
        self.status = status
        self.skills = skills or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert personnel object to dictionary for serialization."""
        return {
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "status": self.status,
            "skills": self.skills
        }
    
    @classmethod
    def from_dict(cls, id: str, data: Dict[str, Any]) -> 'Personnel':
        """Create personnel object from dictionary."""
        return cls(
            id=id,
            name=data["name"],
            role=data["role"],
            department=data["department"],
            status=data["status"],
            skills=data.get("skills", [])
        )


class ResourceManager:
    """Class for managing agricultural resources (machinery and personnel)."""
    
    def __init__(self, data_dir: str = "resource_data"):
        self.data_dir = data_dir
        self.machinery_file = os.path.join(data_dir, "machinery.json")
        self.personnel_file = os.path.join(data_dir, "personnel.json")
        self.usage_log_file = os.path.join(data_dir, "usage_log.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize empty data structures if files don't exist
        if not os.path.exists(self.machinery_file):
            with open(self.machinery_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.personnel_file):
            with open(self.personnel_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.usage_log_file):
            with open(self.usage_log_file, 'w') as f:
                json.dump([], f)
    
    def _load_machinery(self) -> Dict[str, Machinery]:
        """Load machinery data from file."""
        try:
            with open(self.machinery_file, 'r') as f:
                data = json.load(f)
                return {id: Machinery.from_dict(id, item) for id, item in data.items()}
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_machinery(self, machinery: Dict[str, Machinery]) -> None:
        """Save machinery data to file."""
        with open(self.machinery_file, 'w') as f:
            json.dump({id: m.to_dict() for id, m in machinery.items()}, f, indent=2)
    
    def _load_personnel(self) -> Dict[str, Personnel]:
        """Load personnel data from file."""
        try:
            with open(self.personnel_file, 'r') as f:
                data = json.load(f)
                return {id: Personnel.from_dict(id, item) for id, item in data.items()}
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_personnel(self, personnel: Dict[str, Personnel]) -> None:
        """Save personnel data to file."""
        with open(self.personnel_file, 'w') as f:
            json.dump({id: p.to_dict() for id, p in personnel.items()}, f, indent=2)
    
    def _load_usage_log(self) -> List[Dict[str, Any]]:
        """Load usage log data from file."""
        try:
            with open(self.usage_log_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_usage_log(self, log: List[Dict[str, Any]]) -> None:
        """Save usage log data to file."""
        with open(self.usage_log_file, 'w') as f:
            json.dump(log, f, indent=2)
    
    def _log_action(self, resource_type: str, resource_id: str, resource_name: str, 
                   action: str, **kwargs) -> None:
        """Log an action in the usage log."""
        log = self._load_usage_log()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "resource_type": resource_type,
            "resource_id": resource_id,
            "resource_name": resource_name,
            "action": action,
            **kwargs
        }
        log.append(entry)
        self._save_usage_log(log)
    
    # Machinery Management
    
    def register_machinery(self, name: str, type: str, status: str = "available",
                          last_maintenance_date: Optional[str] = None,
                          purchase_date: Optional[str] = None) -> Machinery:
        """Register a new machinery resource."""
        machinery = self._load_machinery()
        new_machinery = Machinery(name, type, status, last_maintenance_date, purchase_date)
        machinery[new_machinery.id] = new_machinery
        self._save_machinery(machinery)
        
        self._log_action(
            resource_type="machinery",
            resource_id=new_machinery.id,
            resource_name=name,
            action="registration",
            details=f"Registered new {type}"
        )
        
        return new_machinery
    
    def update_machinery(self, machinery_id: str, **kwargs) -> Optional[Machinery]:
        """Update an existing machinery resource."""
        machinery = self._load_machinery()
        if machinery_id not in machinery:
            return None
        
        for key, value in kwargs.items():
            if hasattr(machinery[machinery_id], key):
                setattr(machinery[machinery_id], key, value)
        
        self._save_machinery(machinery)
        
        self._log_action(
            resource_type="machinery",
            resource_id=machinery_id,
            resource_name=machinery[machinery_id].name,
            action="update",
            details=f"Updated {', '.join(kwargs.keys())}"
        )
        
        return machinery[machinery_id]
    
    def get_machinery(self, machinery_id: str) -> Optional[Machinery]:
        """Get a specific machinery resource by ID."""
        machinery = self._load_machinery()
        return machinery.get(machinery_id)
    
    def get_all_machinery(self) -> List[Machinery]:
        """Get all machinery resources."""
        return list(self._load_machinery().values())
    
    def get_machinery_by_type(self, type: str) -> List[Machinery]:
        """Get machinery resources by type."""
        machinery = self._load_machinery()
        return [m for m in machinery.values() if m.type == type]
    
    def get_available_machinery(self) -> List[Machinery]:
        """Get available machinery resources."""
        machinery = self._load_machinery()
        return [m for m in machinery.values() if m.status == "available"]
    
    def assign_machinery(self, machinery_id: str, task: str, location: str) -> bool:
        """Assign machinery to a task."""
        machinery = self._load_machinery()
        if machinery_id not in machinery or machinery[machinery_id].status != "available":
            return False
        
        machinery[machinery_id].status = "in_use"
        self._save_machinery(machinery)
        
        self._log_action(
            resource_type="machinery",
            resource_id=machinery_id,
            resource_name=machinery[machinery_id].name,
            action="assignment",
            task=task,
            location=location
        )
        
        return True
    
    def release_machinery(self, machinery_id: str) -> bool:
        """Release machinery from a task."""
        machinery = self._load_machinery()
        if machinery_id not in machinery or machinery[machinery_id].status != "in_use":
            return False
        
        machinery[machinery_id].status = "available"
        self._save_machinery(machinery)
        
        self._log_action(
            resource_type="machinery",
            resource_id=machinery_id,
            resource_name=machinery[machinery_id].name,
            action="release",
            details="Released from task"
        )
        
        return True
    
    def record_maintenance(self, machinery_id: str) -> bool:
        """Record maintenance for machinery."""
        machinery = self._load_machinery()
        if machinery_id not in machinery:
            return False
        
        machinery[machinery_id].last_maintenance_date = datetime.now().isoformat()
        self._save_machinery(machinery)
        
        self._log_action(
            resource_type="machinery",
            resource_id=machinery_id,
            resource_name=machinery[machinery_id].name,
            action="maintenance",
            details="Maintenance performed"
        )
        
        return True
    
    # Personnel Management
    
    def register_personnel(self, name: str, role: str, department: str,
                          status: str = "available", skills: List[str] = None) -> Personnel:
        """Register a new personnel resource."""
        personnel = self._load_personnel()
        new_personnel = Personnel(name, role, department, status, skills)
        personnel[new_personnel.id] = new_personnel
        self._save_personnel(personnel)
        
        self._log_action(
            resource_type="personnel",
            resource_id=new_personnel.id,
            resource_name=name,
            action="registration",
            details=f"Registered new {role}"
        )
        
        return new_personnel
    
    def update_personnel(self, personnel_id: str, **kwargs) -> Optional[Personnel]:
        """Update an existing personnel resource."""
        personnel = self._load_personnel()
        if personnel_id not in personnel:
            return None
        
        for key, value in kwargs.items():
            if hasattr(personnel[personnel_id], key):
                setattr(personnel[personnel_id], key, value)
        
        self._save_personnel(personnel)
        
        self._log_action(
            resource_type="personnel",
            resource_id=personnel_id,
            resource_name=personnel[personnel_id].name,
            action="update",
            details=f"Updated {', '.join(kwargs.keys())}"
        )
        
        return personnel[personnel_id]
    
    def get_personnel(self, personnel_id: str) -> Optional[Personnel]:
        """Get a specific personnel resource by ID."""
        personnel = self._load_personnel()
        return personnel.get(personnel_id)
    
    def get_all_personnel(self) -> List[Personnel]:
        """Get all personnel resources."""
        return list(self._load_personnel().values())
    
    def get_personnel_by_department(self, department: str) -> List[Personnel]:
        """Get personnel resources by department."""
        personnel = self._load_personnel()
        return [p for p in personnel.values() if p.department == department]
    
    def get_personnel_by_skill(self, skill: str) -> List[Personnel]:
        """Get personnel resources by skill."""
        personnel = self._load_personnel()
        return [p for p in personnel.values() if skill in p.skills]
    
    def get_available_personnel(self) -> List[Personnel]:
        """Get available personnel resources."""
        personnel = self._load_personnel()
        return [p for p in personnel.values() if p.status == "available"]
    
    def assign_personnel(self, personnel_id: str, task: str, location: str) -> bool:
        """Assign personnel to a task."""
        personnel = self._load_personnel()
        if personnel_id not in personnel or personnel[personnel_id].status != "available":
            return False
        
        personnel[personnel_id].status = "assigned"
        self._save_personnel(personnel)
        
        self._log_action(
            resource_type="personnel",
            resource_id=personnel_id,
            resource_name=personnel[personnel_id].name,
            action="assignment",
            task=task,
            location=location
        )
        
        return True
    
    def release_personnel(self, personnel_id: str) -> bool:
        """Release personnel from a task."""
        personnel = self._load_personnel()
        if personnel_id not in personnel or personnel[personnel_id].status != "assigned":
            return False
        
        personnel[personnel_id].status = "available"
        self._save_personnel(personnel)
        
        self._log_action(
            resource_type="personnel",
            resource_id=personnel_id,
            resource_name=personnel[personnel_id].name,
            action="release",
            details="Released from task"
        )
        
        return True
    
    # Reporting
    
    def generate_resource_report(self) -> Dict[str, Any]:
        """Generate a report of all resources."""
        machinery = self._load_machinery()
        personnel = self._load_personnel()
        
        return {
            "machinery": {
                "total": len(machinery),
                "available": sum(1 for m in machinery.values() if m.status == "available"),
                "in_use": sum(1 for m in machinery.values() if m.status == "in_use"),
                "by_type": {
                    type: sum(1 for m in machinery.values() if m.type == type)
                    for type in set(m.type for m in machinery.values())
                }
            },
            "personnel": {
                "total": len(personnel),
                "available": sum(1 for p in personnel.values() if p.status == "available"),
                "assigned": sum(1 for p in personnel.values() if p.status == "assigned"),
                "by_department": {
                    dept: sum(1 for p in personnel.values() if p.department == dept)
                    for dept in set(p.department for p in personnel.values())
                }
            }
        }
    
    def get_resource_usage_history(self, resource_type: str = None, 
                                  resource_id: str = None, 
                                  action: str = None) -> List[Dict[str, Any]]:
        """Get resource usage history with optional filters."""
        log = self._load_usage_log()
        
        # Apply filters
        if resource_type:
            log = [entry for entry in log if entry["resource_type"] == resource_type]
        if resource_id:
            log = [entry for entry in log if entry["resource_id"] == resource_id]
        if action:
            log = [entry for entry in log if entry["action"] == action]
        
        return log


class ResourceOptimizer:
    """Class for optimizing resource allocation."""
    
    @staticmethod
    def calculate_machinery_efficiency(machine, task):
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
        if machine.status == 'available':
            efficiency += 0.5
            
        # Age penalty (newer machines are more efficient)
        if machine.purchase_date:
            age_years = (datetime.now() - datetime.strptime(machine.purchase_date, '%Y-%m-%d')).days / 365
            # Cap the age penalty to avoid extreme negative values
            age_penalty = min(age_years, 1.0)
            efficiency -= age_penalty
            
        return efficiency
    
    @staticmethod
    def optimize_machinery_assignment(resource_manager, tasks):
        """Optimize machinery assignment based on task priority and machinery efficiency."""
        available_machinery = resource_manager.get_available_machinery()
        assignments = {}
        
        # Sort tasks by priority (higher priority first)
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        
        for task in sorted_tasks:
            if not available_machinery:
                break
            
            # First, try to find machines of the matching type
            matching_machines = [m for m in available_machinery if m.type == task.type]
            
            # If no matching machines are available, use all available machines
            machines_to_consider = matching_machines if matching_machines else available_machinery
            
            # If we have machines to consider
            if machines_to_consider:
                # Calculate efficiency for each available machine
                efficiencies = [
                    (machine, ResourceOptimizer.calculate_machinery_efficiency(machine, task))
                    for machine in machines_to_consider
                ]
                
                # Sort by efficiency (higher efficiency first)
                efficiencies.sort(key=lambda x: x[1], reverse=True)
                
                # Assign the most efficient machine
                best_machine, _ = efficiencies[0]
                assignments[task.id] = best_machine.id
                
                # Remove assigned machine from available list
                available_machinery = [m for m in available_machinery if m.id != best_machine.id]
        
        return assignments
    
    @staticmethod
    def resolve_assignment_conflicts(resource_manager, assignments, priorities):
        """Resolve conflicts in resource assignments based on task priorities."""
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
