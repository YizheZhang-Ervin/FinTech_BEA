# BEA  
**Black Eight Agency-Gold Analysis System**  
  
## Before Run this Project  
* please install the required python libs  
    pip install -r requirements.txt
  
## Run Project Instruction
Run By Terminal:
#### For development environment:  
* this mode will listen on port: 8000  
    BEA path > python server.py --env=develop  
#### For deployment and produce environment:  
* this mode will listen on port: 80  
    BEA path > python server.py --env=produce  

## Other optional parameters
* --port  
= 8000[default choice]  
* --env  
= develop[default choice]  
= produce  
* --processtype  
= single[default choice]  
= multiple  