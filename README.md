====================================
DDL Incubator 3, Team 7, Censusables
====================================



Build notes
===========

Since this project uses scikit-learn, I would recommend installing the [Anaconda]
(https://www.continuum.io/downloads) package. Then, for most packages, you can use
conda to install additional packages. However, Anaconda does not play well with
virtualenv.

If you choose not to install Anaconda, for Mac and Linux, you need development
tools and libraries installed. You will need to install a Fortran compiler by
installing gcc:

    liblapack-dev
    gfortan

I suspect this won't be an issue on Linux, assuming you have gcc
installed.  For Windows, pip and buildout will be downloading binary
distributions.

Basic packages you will need:

    requests
    matplotlib
    numpy
    scikit-learn
    pandas
    Flask
    vincent
    gunicorn

Application
===========

Censusables is a basic Flask web application that allows a user to
weight preferences of Average Income, Housing Cost, Diversity, and
Population Density to identify zip code neighborhoods that are the
best fit his/her selections.

The application uses a combination of [US Census (American Community
Survey 5 year)](https://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html)
data downloaded from [NHGIS] (https://www.nhgis.org/)
and [Zillow](http://www.zillow.com/research/data/) housing and rental data.

Data Model
----------

The application uses Pandas' DataFrames and Scikit-learn's Principal Component
Package to standardize and create 4 separate principal component analyses for each
of the above parameters. The first principal component of each analsysis is used as
an index on each zip code. These indexes are then normalized on a scale of 0 to 1.
Based on the values of the web sliders, the application will determine the zip codes
that are the closest fit to the 4 variables. If no state is selected, a heat map of
US is diplayed. The darker colors represent the zip codes that are a closer match to
the selections. The top 5 zip codes are displayed on the page. If a state is selected,
the data is filtered, diplaying a state map and the top 5 zip codes of that state.

Visualizations
--------------

The maps use topo.json files and Vincent to display the visualizations.

Example
-------

A sample application has been deployed to Heroku [HERE](https://blooming-wildwood-5949.herokuapp.com/).
