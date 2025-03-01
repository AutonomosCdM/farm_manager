import typer
from typer.testing import CliRunner
from farm_manager.cli import app

runner = CliRunner()

def test_workflow_command():
    """Test the workflow subcommand."""
    result = runner.invoke(app, [
        'workflow', 
        '--operation', 'planting', 
        '--crop-type', 'avellano', 
        '--area', '5.5', 
        '--date', '2025-07-15'
    ])
    assert result.exit_code == 0
    assert "Plan de Planting" in result.output

def test_irrigate_command():
    """Test the irrigate subcommand."""
    result = runner.invoke(app, [
        'irrigate', 
        '--crop', 'trigo', 
        '--area', '10.0'
    ])
    assert result.exit_code == 0
    assert "Plan de Riego" in result.output

def test_weather_command():
    """Test the weather subcommand."""
    result = runner.invoke(app, [
        'weather', 
        '--location', 'Santiago', 
        '--days', '3'
    ])
    assert result.exit_code == 0
    assert "Pronóstico del Tiempo" in result.output

def test_resources_list_command():
    """Test the resources list subcommand."""
    result = runner.invoke(app, [
        'resources', 
        '--action', 'list', 
        '--resource-type', 'machinery'
    ])
    assert result.exit_code == 0
    assert "Recursos Disponibles" in result.output

def test_resources_optimize_command():
    """Test the resources optimize subcommand."""
    result = runner.invoke(app, [
        'resources', 
        '--action', 'optimize', 
        '--resource-type', 'personnel'
    ])
    assert result.exit_code == 0
    assert "Resultado de Optimización" in result.output

def test_invalid_workflow_command():
    """Test handling of invalid workflow command."""
    result = runner.invoke(app, [
        'workflow', 
        '--operation', 'invalid', 
        '--crop-type', 'test', 
        '--area', '1.0', 
        '--date', '2025-01-01'
    ])
    assert result.exit_code != 0
    assert "Error" in result.output
