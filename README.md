# plot_socib_rv_adcp
The plot_socib_rv_adcp is a set of python scripts and functions developed at SOCIB to manage the data collected by a VM-ADCP mounted onboard the SOCIB Research Vessel. They are able to plot the main variables (including QC variables) stored into the SOCIB netcdf files and plot them over the time dimension

##Prerequisites:

    See requirements file for extralibraries needed.
    Customize matplotlibrc settings (https://matplotlib.org/tutorials/introductory/customizing.html)

## The following features are already implemented in the toolbox:

    One main script to perform data processing:
        main.py
    Two processing functions to perform both connection and reading of database metadata and plotting the variables of the file:
        dbConnect.py
        plotNcVars

## The following features are planned or in development:

    calculate data quality statistics using the following script:
        calculateDataStatistics.py

## Copyright

Copyright (C) 2013-2018 ICTS SOCIB - Servei d'observació i predicció costaner de les Illes Balears http://www.socib.es

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
