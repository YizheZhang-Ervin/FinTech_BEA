# BEA  
**Black Eight Agency-Gold Visualization System**  
  
## Before Run this Project  
#### virtual environments  
    virtualenvDirectory > activate  (virtualenv)  
    workon virtualenvName  (virtualenvwrapper)  
#### please install the required python libs  
    pip install -r requirements.txt  
  
## Run Project Instruction  
Run By Terminal:  
#### For development environment:  
    BEA path > python manage.py  (default port:8000)  
#### For deployment and produce environment:  
    BEA path > python manage.py --env=produce  --port=80  (formal port:80)  

## All optional parameters
* --port  
= 8000 [default]  
* --env  
= develop [default]  
= produce  
* --processtype  
= single [default]  
= multiple  
* --daemon  
= off [default]  
= on  

## Data
1. Trend Plots & Tables  
    * Time-slicing  
        Days: Quandl API  
        1 Wweeks - 3months: Sqlite  
        6months - 12years: Sqlite  
    * DIY Plots: Sqlite  
2. Animation: Sqlite  
3. 3D Plots: Sqlite  

## Function
Gold Price Visualization  
JavaScript CMD  
Python CMD  
Sql CMD  
Html CMD  
Mirror  
Translator  
Web Parameter  
World Map  
Prevent Right Click  
