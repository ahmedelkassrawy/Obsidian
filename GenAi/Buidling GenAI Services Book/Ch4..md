Introduction to Type Safety
Types in programming specify what values can be assigned to varables and operations , that can be perfomrned on those varaubales

In python common types are :
- Integer , Float  String , Boolean

Type safety is a practice that ensures that variables are only assigned values compabitle with their defined types

Since python is a dynamically typed language means that types are checked only when you run the code and not in advance , also you dtont have to explicitly declare types as they can be inferred as you assign values to variables.

But using typing , we can catch errors more quickly

we can enforce type constraints by declaring fully typed variables and functions
![[Pasted image 20260929141426.png]]

Type checkers can immediately raise warnings to help you address such changes during development.

As a result, type safety practices can save you time with early detection and prevent you from dealing with more obscure runtime errors

Finally, you can go one step further to set up automatic type checks in your deployment pipeline to prevent pushing breaking changes to production environments. Type safety at first seems like a burden. You have to explicitly type each and every function you write, which can be a hassle and slow you down in the initial phases of development

When you don’t use types, you open yourself to all sorts of bugs and errors that might occur because other developers unexpectedly updated the database tables or API schemas that your service interacts with.

. The syntax that allows you to declare these types is type annotation.

In Python applications, type annotations are used for: Code editor auto-complete support Static type checks using tools like mypy FastAPI also leverages types hints to: Define handler requirements including path and query parameters, bodies, headers, and dependencies, etc. Convert data whenever needed Validate data from incoming requests, databases, and external services Auto-update the OpenAPI specification that powers the generated documentation page