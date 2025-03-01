import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

# Import modules for subcommands
from farm_manager.workflows import (
    WorkflowTemplateManager,
    PlantingTemplate,
    HarvestTemplate,
    MaintenanceTemplate,
)
from farm_manager.irrigation.decision_system import IrrigationDecisionSystem
from farm_manager.weather.client import WeatherClient
from farm_manager.resources.manager import ResourceManager

# Create main app
app = typer.Typer(
    name="farm-manager",
    help="Herramienta integral de gestión agrícola",
    rich_help_panel="rich",
)

# Create console for rich output
console = Console()


# Workflow subcommand
@app.command()
def workflow(
    operation: str = typer.Option(..., help="Tipo de operación (planting, harvest, maintenance)"),
    crop_type: str = typer.Option(..., help="Tipo de cultivo"),
    area: float = typer.Option(..., help="Área en hectáreas"),
    date: str = typer.Option(..., help="Fecha de la operación"),
):
    """
    Generar un plan de flujo de trabajo para operaciones agrícolas.
    """
    try:
        manager = WorkflowTemplateManager()

        # Prepare context based on operation type
        context = {"crop_type": crop_type, "area_hectares": area}

        if operation == "planting":
            context.update(
                {
                    "soil_type": typer.prompt("Tipo de suelo", default="franco"),
                    "planting_date": date,
                }
            )
        elif operation == "harvest":
            context.update(
                {
                    "expected_yield": typer.prompt("Rendimiento esperado por hectárea", type=float),
                    "harvest_date": date,
                }
            )
        elif operation == "maintenance":
            context.update(
                {
                    "maintenance_type": typer.prompt(
                        "Tipo de mantenimiento (irrigation/fertilization/pest_control)",
                        default="maintenance",
                    ),
                    "maintenance_date": date,
                }
            )
        else:
            console.print(f"[bold red]Error:[/] Operación no válida: {operation}")
            raise typer.Abort()

        # Generate workflow
        workflow_plan = manager.generate_workflow(operation, context)

        # Display workflow plan
        console.print(f"\n[bold green]Plan de {operation.capitalize()}:[/]")
        table = Table(title=f"Detalles del Flujo de Trabajo - {operation.capitalize()}")

        # Add columns dynamically based on workflow type
        for key, value in workflow_plan.items():
            if isinstance(value, (str, int, float)):
                table.add_row(str(key), str(value))
            elif isinstance(value, list):
                table.add_row(str(key), ", ".join(map(str, value)))
            elif isinstance(value, dict):
                table.add_row(str(key), ", ".join(f"{k}: {v}" for k, v in value.items()))

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Abort()


# Irrigation subcommand
@app.command()
def irrigate(
    crop: str = typer.Option(..., help="Tipo de cultivo"),
    area: float = typer.Option(..., help="Área en hectáreas"),
):
    """
    Tomar decisiones de riego basadas en datos agrícolas.
    """
    try:
        decision_system = IrrigationDecisionSystem()
        irrigation_plan = decision_system.generate_irrigation_plan(crop, area)

        console.print("\n[bold green]Plan de Riego:[/]")
        table = Table(title="Detalles del Plan de Riego")

        for key, value in irrigation_plan.items():
            table.add_row(str(key), str(value))

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Abort()


# Weather subcommand
@app.command()
def weather(
    location: str = typer.Option(..., help="Ubicación para consultar el clima"),
    days: int = typer.Option(3, help="Número de días de pronóstico"),
):
    """
    Obtener información meteorológica para una ubicación.
    """
    try:
        client = WeatherClient()
        forecast = client.get_forecast(location, days)

        console.print(f"\n[bold green]Pronóstico del Tiempo para {location}:[/]")
        table = Table(title=f"Pronóstico a {days} días")

        for day in forecast:
            table.add_row(
                day.get("date", "N/A"),
                day.get("temperature", "N/A"),
                day.get("conditions", "N/A"),
            )

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Abort()


# Resources subcommand
@app.command()
def resources(
    action: str = typer.Option(..., help="Acción a realizar (list/optimize)"),
    resource_type: Optional[str] = typer.Option(None, help="Tipo de recurso"),
):
    """
    Gestionar y optimizar recursos agrícolas.
    """
    try:
        manager = ResourceManager()

        if action == "list":
            resources = manager.list_resources(resource_type)

            console.print("\n[bold green]Recursos Disponibles:[/]")
            table = Table(title="Inventario de Recursos")

            for resource in resources:
                table.add_row(
                    resource.get("type", "N/A"),
                    resource.get("name", "N/A"),
                    str(resource.get("quantity", "N/A")),
                )

            console.print(table)

        elif action == "optimize":
            optimization_result = manager.optimize_resources(resource_type)

            console.print("\n[bold green]Resultado de Optimización:[/]")
            table = Table(title="Optimización de Recursos")

            for key, value in optimization_result.items():
                table.add_row(str(key), str(value))

            console.print(table)

        else:
            console.print(f"[bold red]Error:[/] Acción no válida: {action}")
            raise typer.Abort()

    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Abort()


def main():
    """
    Punto de entrada principal para la CLI de Farm Manager.
    """
    app()


if __name__ == "__main__":
    main()
