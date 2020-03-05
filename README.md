# BEA  
**Black Eight Agency-Gold Analysis System**  
  
## Before Run this Project  
* please install the required python libs  
    pip install -r requirements.txt
  
## Run Project Instruction
Run By Terminal:
#### For development environment:  
* this mode will listen on port: 8000  
    BEA path > python manage.py  
#### For deployment and produce environment:  
* this mode will listen on port: 80  
    BEA path > python manage.py --env=produce  --port=80  

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