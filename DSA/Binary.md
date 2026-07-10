|             |     |        |                                    |
| ----------- | --- | ------ | ---------------------------------- |
| left shift  | <<  | x << y | all bits in x shifted left y bits  |
| right shift | >>  | x >> y | all bits in x shifted right y bits |
| bitwise NOT | ~   | ~x     | all bits in x flipped              |
| bitwise AND | &   | x & y  | each bit in x AND each bit in y    |
| bitwise OR  | \|  | x \| y | each bit in x OR each bit in y     |
| bitwise XOR | ^   | x ^ y  | each bit in x XOR each bit in y    |

XOR --> 3ayz wa7da l48ala.
A **bit mask** is a predefined set of bits that is used to select which specific bits will be modified by subsequent operations.

setting a bit you have to use a mask first 
```C++
#include <cstdint>
#include <iostream>

int main()
{
    [[maybe_unused]] constexpr std::uint8_t mask0{ 0b0000'0001 }; // represents bit 0
    [[maybe_unused]] constexpr std::uint8_t mask1{ 0b0000'0010 }; // represents bit 1
    [[maybe_unused]] constexpr std::uint8_t mask2{ 0b0000'0100 }; // represents bit 2
    [[maybe_unused]] constexpr std::uint8_t mask3{ 0b0000'1000 }; // represents bit 3
    [[maybe_unused]] constexpr std::uint8_t mask4{ 0b0001'0000 }; // represents bit 4
    [[maybe_unused]] constexpr std::uint8_t mask5{ 0b0010'0000 }; // represents bit 5
    [[maybe_unused]] constexpr std::uint8_t mask6{ 0b0100'0000 }; // represents bit 6
    [[maybe_unused]] constexpr std::uint8_t mask7{ 0b1000'0000 }; // represents bit 7

    std::uint8_t flags{ 0b0000'0101 }; // 8 bits in size means room for 8 flags

    std::cout << "bit 1 is " << (static_cast<bool>(flags & mask1) ? "on\n" : "off\n");

    flags |= mask1; // turn on bit 1

    std::cout << "bit 1 is " << (static_cast<bool>(flags & mask1) ? "on\n" : "off\n");

    return 0;
}
```

to set a bit use OR.
```C++
flags |= (mask4 | mask5); // turn bits 4 and 5 on at the same time
```

reset 
```C++
flags &= ~mask2; // turn off bit 2
```
```C++
flags &= ~(mask4 | mask5); // turn bits 4 and 5 off at the same time
```

flipping
```C++
flags ^= mask2;
```

test
```C++
```cpp
flags.test(1)
```
```
