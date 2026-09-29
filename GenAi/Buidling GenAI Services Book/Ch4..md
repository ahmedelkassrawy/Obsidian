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

```python
# utils.py

from typing import Literal,TypeAlias
from loguru import logger
import tiktoken

SupportedModels: TypeAlias = Literal["gpt-3.5","gpt-4"]
PriceTable: TypeAlias = dict[SupportedModels,float]

price_table = PriceTable = {
    "gpt-3.5": 0.002,
    "gpt-4": 0.06
}

def count_tokens(text:str | None) -> int:
    if text is None:
        logger.warning("Response is None")
        return 0

    enc = tiktoken.encoding_for_model("gpt-3.5")
    return len(enc.encode(text))

def calculate_usage_costs(
        prompt:str , response:str | None,
        model: SupportedModels
) -> tuple[float,float,float]:
    if model not in price_table:
        raise ValueError(f"Model {model} is not supported. Supported models are: {list(price_table.keys())}")

    price = price_table[model]
    req_costs = price * count_tokens(prompt) / 1000
    res_costs = price * count_tokens(response) / 1000
    total_costs = req_costs + res_costs

    return req_costs, res_costs, total_costs
```

- `TypeAlias` explicitly marks a variable assignment as a **type alias** rather than an ordinary variable assignment.
- Literal allows us to specify that variable should hold some specific value from these inside the list

Instead of TypeAlias we now use the Annotated , it reuses types but it allows you to define metadata for types

metadata doesn't affect the type checkers but is useful for code documentation 

Keep in mind that the Annotated feature requires a minimum of two arguments to work

```python
SupportedModels = Annotated[Literal["gpt-3.5","gpt-40]]
PricesTable = Annotated[dict[SupportedModel,float]]

price: PriceTable = {
	"gpt-3.5": 0.00638,
	"gpt-40": 0.000638
}
```

---
Dataclasses 
if we need custom data structures , we can use dataclass to organize and store and transfer data accross the application

Having a dataclass allows you to organize your data in a custom-defined structure and pass it as a single item to functions that require data from different places

