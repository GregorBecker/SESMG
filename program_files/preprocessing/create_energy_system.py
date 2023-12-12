# -*- coding: utf-8 -*-
"""
    Functions for creating an oemof energy system.

    Christian Klemm - christian.klemm@fh-muenster.de
"""
import pandas
import logging
from program_files.preprocessing.import_weather_data \
    import import_open_fred_weather_data
from oemof.solph import EnergySystem
import random as rand
pandas.options.mode.chained_assignment = None


def import_model_definition(filepath: str, delete_units=True) -> dict:
    """
        Imports data from a spreadsheet model definition file.
    
        The excel sheet has to contain the following sheets:
    
            - energysystem
            - buses
            - transformers
            - sinks
            - sources
            - storages
            - links
            - time series
            - weather data
            - competition constraints
            - insulation
            - district heating
            - pipe types
    
        :param filepath: path to excel model definition file
        :type filepath: str
        :param delete_units: boolean which defines rather the unit \
            row in the imported spreadsheets is removed or not
        :type delete_units: bool
    
        :raises: - **FileNotFoundError** - excel spreadsheet not found
    
        :return: - **nodes_data** (dict) - dictionary containing excel sheets
    """
    # creates nodes from excel sheet
    try:
        xls = pandas.ExcelFile(filepath)
    except FileNotFoundError:
        raise FileNotFoundError("Problem importing model definition file.")
    
    nodes_data = {
        "buses": xls.parse("buses"),
        "energysystem": xls.parse("energysystem"),
        "sinks": xls.parse("sinks"),
        "links": xls.parse("links"),
        "sources": xls.parse("sources"),
        "timeseries": xls.parse("time series", parse_dates=["timestamp"]),
        "transformers": xls.parse("transformers"),
        "storages": xls.parse("storages"),
        "weather data": xls.parse("weather data", parse_dates=["timestamp"]),
        "competition constraints": xls.parse("competition constraints"),
        "insulation": xls.parse("insulation"),
        "district heating": xls.parse("district heating"),
        "pipe types": xls.parse("pipe types")
    }
    if delete_units:
        # delete spreadsheet row within technology or units specific
        # parameters
        for index in nodes_data.keys():
            if index not in ["timeseries", "weather data"] \
                    and len(nodes_data[index]) > 0:
                nodes_data[index] = nodes_data[index].drop(index=0)
    
    # returns logging info
    logging.info("\t Spreadsheet scenario successfully imported.")
    # if the user imported coordinates for the OpenFred weather data
    # download the import algorithm is triggered
    if nodes_data["energysystem"].loc[1, "weather data lat"] \
            not in ["None", "none"]:
        logging.info("\t Start import weather data")
        lat = nodes_data["energysystem"].loc[1, "weather data lat"]
        lon = nodes_data["energysystem"].loc[1, "weather data lon"]
        nodes_data = import_open_fred_weather_data(nodes_data, lat, lon)
    # returns nodes data
    return nodes_data


def import_model_definition_montecarlo(durchlauf: int, montecarlo_section_runs: int,
                            montecarlo_section: int,
                            filepath: str, delete_units=True) -> dict:
    """
        Imports data from a spreadsheet model definition file.
    
        The excel sheet has to contain the following sheets:
    
            - energysystem
            - buses
            - transformers
            - sinks
            - sources
            - storages
            - links
            - time series
            - weather data
            - competition constraints
            - insulation
            - district heating
            - pipe types
    
        :param filepath: path to excel model definition file
        :type filepath: str
        :param delete_units: boolean which defines rather the unit \
            row in the imported spreadsheets is removed or not
        :type delete_units: bool
    
        :raises: - **FileNotFoundError** - excel spreadsheet not found
    
        :return: - **nodes_data** (dict) - dictionary containing excel sheets
    """
    # creates nodes from excel sheet
    try:
        xls = pandas.ExcelFile(filepath)  
    except FileNotFoundError:
        raise FileNotFoundError("Problem importing model definition file.")
        
    if durchlauf>=montecarlo_section_runs*(montecarlo_section-1) and durchlauf<montecarlo_section_runs*montecarlo_section:
        
        ## Eigene Bearbeitung Start

        # Ändern der Kapazitäten durch Zufallszahlen, kommt bei "sources" rein, im aktuellen Zustand nicht zur Variation gesetzt

        a = xls.parse("sources")
        a_2 = xls.parse("sources")
        

        # Änderung des Heizungssystems auf Zufallsbasis von der Wahl der Komponente als auch der Kapazität, bei "transformers"

        b = xls.parse("transformers")
        b_2 = xls.parse("transformers")
        for i, index in b["min. investment capacity"][1:].items():
            index=rand.randint(0,b_2["max. investment capacity"][i])
            b["min. investment capacity"][i]=index
            b["max. investment capacity"][i]=b["min. investment capacity"][i]
            logging.info("Transformers: " + str(index))
       


        # Zufällige Auswahl von Speichersystemen, thermisch und/oder elektrisch

        c = xls.parse("storages")
        c_2 = xls.parse("storages")
        for i, index in c["min. investment capacity"][1:].items():
            index=rand.randint(0,c_2["max. investment capacity"][i])
            c["min. investment capacity"][i]=index
            c["max. investment capacity"][i]=c["min. investment capacity"][i]
            logging.info("... und Speicher: " + str(index))

        

        nodes_data = {
        "buses": xls.parse("buses"),
        "energysystem": xls.parse("energysystem"),
        "sinks": xls.parse("sinks"),
        "links": xls.parse("links"),
        "sources": a,
        "timeseries": xls.parse("time series", parse_dates=["timestamp"]),
        "transformers": b,
        "storages": c,
        "weather data": xls.parse("weather data", parse_dates=["timestamp"]),
        "competition constraints": xls.parse("competition constraints"),
        "insulation": xls.parse("insulation"),
        "district heating": xls.parse("district heating"),
        "pipe types": xls.parse("pipe types")
        }
        if delete_units:
            # delete spreadsheet row within technology or units specific
            # parameters
            for index in nodes_data.keys():
                if index not in ["timeseries", "weather data"] \
                        and len(nodes_data[index]) > 0:
                    nodes_data[index] = nodes_data[index].drop(index=0)

        # returns logging info
        logging.info("\t Spreadsheet scenario successfully imported.")
        # if the user imported coordinates for the OpenFred weather data
        # download the import algorithm is triggered
        if nodes_data["energysystem"].loc[1, "weather data lat"] \
                not in ["None", "none"]:
            logging.info("\t Start import weather data")
            lat = nodes_data["energysystem"].loc[1, "weather data lat"]
            lon = nodes_data["energysystem"].loc[1, "weather data lon"]
            nodes_data = import_open_fred_weather_data(nodes_data, lat, lon)
        # returns nodes data
        return nodes_data   
            
    else:
        
        
        a = xls.parse("sources")
        a_2 = xls.parse("sources")
        


        b = xls.parse("transformers")
        b_2 = xls.parse("transformers")
        for i, index in b["min. investment capacity"][1:].items():
            index=rand.randint(0,b_2["max. investment capacity"][i])
            b["min. investment capacity"][i]=index
            b["max. investment capacity"][i]=b["min. investment capacity"][i]
            logging.info("Transformers: " + str(index))
        

        c = xls.parse("storages")
        c_2 = xls.parse("storages")
        for i, index in c["min. investment capacity"][1:].items():
            index=rand.randint(0,c_2["max. investment capacity"][i])
            c["min. investment capacity"][i]=index
            c["max. investment capacity"][i]=c["min. investment capacity"][i]
            logging.info("... und Speicher: " + str(index))

        
        nodes_data={}
        return nodes_data


def define_energy_system(nodes_data: dict) -> EnergySystem:
    """
        Creates an energy system with the parameters defined in the
        given .xlsx-file. The file has to contain a sheet called
        "energysystem", which has to be structured as follows:
    
        +-------------------+-------------------+-------------------+
        |start_date         |end_date           |temporal resolution|
        +-------------------+-------------------+-------------------+
        |YYYY-MM-DD hh:mm:ss|YYYY-MM-DD hh:mm:ss|h                  |
        +-------------------+-------------------+-------------------+
    
        :param nodes_data: dictionary containing data from excel model \
            definition file
        :type nodes_data: dict
        
        :return: **esys** (oemof.solph.Energysystem) - oemof energy \
            system
    """
    # fix pyomo error while using the streamlit gui
    import pyutilib.subprocess.GlobalData
    pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False
    
    # Importing energysystem parameters from the scenario
    row = next(nodes_data["energysystem"].iterrows())[1]
    temp_resolution = row["temporal resolution"]
    timezone = row["timezone"]
    start_date = row["start date"]
    end_date = row["end date"]
    
    # creates time index
    datetime_index = pandas.date_range(start=start_date,
                                       end=end_date,
                                       freq=temp_resolution)
    
    # initialisation of the energy system
    esys = EnergySystem(timeindex=datetime_index)
    # setting the index column for time series and weather data
    for sheet in ["timeseries", "weather data"]:
        # defines a time series
        nodes_data[sheet].set_index("timestamp", inplace=True)
        nodes_data[sheet].index = \
            pandas.to_datetime(nodes_data[sheet].index.values, utc=True)
        nodes_data[sheet].index = \
            pandas.to_datetime(nodes_data[sheet].index).tz_convert(timezone)
    
    # returns logging info
    logging.info(
            "Date time index successfully defined:\n start date:          "
            + str(start_date)
            + ",\n end date:            "
            + str(end_date)
            + ",\n temporal resolution: "
            + str(temp_resolution)
    )
    
    # returns oemof energy system as result of this function
    return esys
