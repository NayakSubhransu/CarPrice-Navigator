import pickle
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

def load_model(model_path='LinearRegressionModel.pkl'):
    return pickle.load(open(model_path, 'rb'))

def load_data(data_path='Cleaned_Car_data.csv'):
    return pd.read_csv(data_path)

def predict_price(model, car_data):
    prediction = model.predict(car_data)
    return np.round(prediction[0], 2)

def list_options(data, column):
    options = sorted(data[column].unique())
    return options

def print_options(console, title, options):
    table = Table(show_header=True, header_style="bold magenta", title=title)
    table.add_column("Index", style="dim", justify="right")
    table.add_column("Option", style="bold yellow")

    for i, option in enumerate(options, start=1):
        table.add_row(str(i), option)

    console.print(table)

def get_user_choice(console, title, options):
    console.print("\n[bold cyan]{}[/bold cyan]".format(title))
    print_options(console, "", options)

    while True:
        try:
            choice = int(console.input("\n[bold cyan]Enter your choice (1-{}):[/bold cyan] ".format(len(options))))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                console.print("[red]Invalid choice.[/red] Please enter a number between 1 and {}.".format(len(options)))
        except ValueError:
            console.print("[red]Invalid input.[/red] Please enter a valid number.")

def main():
    model_path = 'LinearRegressionModel.pkl'
    data_path = 'Cleaned_Car_data.csv'

    model = load_model(model_path)
    car_data = load_data(data_path)
    console = Console()

    # console.print(Panel(
    #     Text("Car Price Prediction CLI").center(80).bold(),
    #     title="Welcome",
    #     border_style="green",
    # ))
    console.print(
        Panel("[bold cyan]Car Price Prediction CLI[/bold cyan]", title="Welcome", border_style="green")
    )


    companies = list_options(car_data, 'company')
    selected_company = get_user_choice(console, "List of available companies:", companies)

    car_models = list_options(car_data[car_data['company'] == selected_company], 'name')
    selected_car_model = get_user_choice(console, "List of available car models:", car_models)

    fuel_types = list_options(car_data, 'fuel_type')
    selected_fuel_type = get_user_choice(console, "List of available fuel types:", fuel_types)

    year = console.input("\n[bold cyan]Enter the manufacturing year of the car:[/bold cyan] ")
    driven = console.input("\n[bold cyan]Enter the kilometers driven:[/bold cyan] ")

    car_data = pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                            data=[[selected_car_model, selected_company, year, driven, selected_fuel_type]])

    prediction = predict_price(model, car_data)
    # Create a table
    table = Table(show_header=False, box=box.SQUARE)
    table.add_column("Attribute", style="bold", justify="right", width=20)
    table.add_column("Value")

# Add rows with enhanced formatting
    table.add_row("[bold yellow]Car Company[/bold yellow]:", f"[bold green]{selected_company}[/bold green]")
    table.add_row("[bold magenta]Car Model[/bold magenta]:", f"[bold red]{selected_car_model}[/bold red]")
    table.add_row("[bold red]Manufacturing Year[/bold red]:", f"[bold magenta]{year}[/bold magenta]")
    table.add_row("[underline green]Predicted Price[/underline green]:", f"[underline yellow]₹{prediction:.2f}[/underline yellow]")
    console.print(table)
   
    
    # table.add_row("[cyan]Car Company[/cyan]:", selected_company)
    # table.add_row("[magenta]Car Model[/magenta]:", selected_car_model)
    # table.add_row("[red]Manufacturing Year of the Car[/red]:", str(year))
    # table.add_row("[underline green]Predicted Price[/underline green]:", f"₹{prediction}")
    
    
          
          
          
if __name__ == '__main__':
    main()
