Results
*************************************************

Interactive Results
=================================================

If the Spreadsheet Energy System Model Generator was executed via the exe.cmd-file, 
a browser window with interactive results will be opened automatically after successful 
modeling. Alternatively, the results of the last modelling run can be accessed by executing the 
Interactive_Results.py file.

.. figure:: ../images/manual/Results/interactive_results2.png
   :width: 100 %
   :alt: interactive_results
   :align: center

   Screenshots of the interactive results browser interface

The results interface has the following elements:

- **Table with a summary of the modelling (1).**
   - Total System Costs: Total costs of the primary optimization criterion (in the example: total monetary costs).
   - Total Constraint Costs: Total costs of the secondary optimization criterion (in the example: total carbon dioxide emissions).
   - Total Variable Costs: Costs per kWh transformed/used/supplied energy
   - Total Periodical Costs: Annual costs per kW(h) of invested plant capacity (only applied for invested capacity, not for existing capacity)
   - Total Energy Demand: Total energy demand of the systems' sinks.
   - Total Energy Usage: Total energy inserted to the energy system (via sources).

- **Graph of the energy system (2).**

- **Table with information about every component (3):** The entries can be filtered and sorted according to their content.

- **Plot, where time series of the different components can be shown (5).** With the help of a selection window (drop-down menu and search function) (4) time series to be shown can be selected. With the help of a number of tools (6) the graphs can be scaled, sections can be displayed and images can be saved.


Results as Spreadsheets and Log-Files
=================================================

The results of the modeling are stored in the "results" folder in two formats:
- as summarizing log files, under
- as detailed xlsx-files.

The log-file gives an overview of which components are created and which of the investment options should be implemented. 
In addition, it is indicated which costs for the supply of the energy system are incurred in the optimized case.
For each implemented bus, an xlsx-file is created in which incoming and outgoing energy flows are specified for each time step of the model 
are.
