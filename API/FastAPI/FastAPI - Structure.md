#### Flat Structure
A flat structure is one in which the application files remain at the root of your project with no nested directories. You may group all your files under a single directory for better organization. The main idea here is to keep all similar code in modules and placed together near the root of your project. For instance, put all your database models in models.py or your endpoints in routes.py.

![[Pasted image 20260122194355.png]]

#### Nested Structure 
The nested structure groups similar modules into packages—effectively creating a nested structure and hierarchy of modules. You group all modules under a package that are similar in nature irrespective of the feature they support. These are loosely coupled modules that contain similar logic for different entities in your project. For instance, the models package may contain users and profiles database models

![[Pasted image 20260122194509.png]]

#### Modular Structure
In the modular structure, modules that are closely related and refer to a specific domain are grouped together. This approach differs from the previously mentioned nested structure. An example could be the users package that contains user schemas, database services, dependencies and routers.

![[Pasted image 20260122194558.png]]

1. Flat
If you are starting with a new project and the complexity of your system is not yet clear, you can focus on writing all your FastAPI code in a single file before worrying about the project structure. You then extract your code into several files under the root directory. This is the initial structure you will adopt when experimenting on the first version of your service from scratch.

2. Nested
As the number of files in your codebase and service complexity grows, you can adopt the nested structure. You can search for files based on logical grouping (models, routers, schemas, etc.) and do not have to worry too much about logical couplings in your code. As you make changes, only a handful of files are affected. At this point, you have an AI microservice.

3. Modular
As you move from a microservice to a full backend service, you will want to adopt a modular structure. There is now an increasing number of modules, features, and complexity. You start grouping your code into packages based on areas of concern. Your code is now handling requests, authentication, external systems, etc., while serving an AI model.

![[Pasted image 20260122203832.png]]
![[Pasted image 20260122203915.png]]