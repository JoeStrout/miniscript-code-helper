# Straight Code Generation

## List reversal

**User:** Write a MiniScript function to reverse a list.

**Assistant:**
```
reverse = function(lst)                                                                                                                      
    result = []                                                                                                                          
    for i in range(lst.len - 1, 0, -1)                                                                                                     
        result.push lst[i]                                                                                                             
    end for                                                                                                                                
    return result                                                                                                                        
end function
```
  Usage:
```
  print reverse([1, 2, 3, 4, 5])  // [5, 4, 3, 2, 1]
```
Note the explicit -1 step in `range(lst.len - 1, 0, -1)` to ensure it returns [] for an empty list rather than counting up.

## Letter frequencies

**User:** Write a MiniScript function to count word frequencies in a string.

**Assistant:**
```
wordFreqs = function(s)                                                                                                                      
    freq = {}                                                                                                                              
    for word in s.split                                                                                                                    
        word = word.lower                                                                                                              
        if freq.hasIndex(word) then                                                                                                    
            freq[word] += 1
        else
            freq[word] = 1
        end if
    end for
    return freq
end function
```
  Usage:
```
result = wordFreqs("The cat sat on the mat the cat")
for kv in result
    print kv.key + ": " + kv.value
end for
// the: 3
// cat: 2
// sat: 1
// on: 1
// mat: 1
```
A few things to note:
- `s.split` with no arguments splits on spaces
- `word.lower` normalizes case so "The" and "the" count together
- `hasIndex` on a map checks if a key exists

## CSV parsing

**User:** Write a MiniScript function that takes CSV data as a list of strings (one string per line), and returns a list of rows as maps.  Assume the first line is headers.

**Assistant:**
```
parseCSV = function(lines)                                                                                                                   
    if lines.len < 2 then return []                                                                                                        
    headers = lines.pull.split(",")                                                                                                          
    for i in headers.indexes
        headers[i] = headers[i].trim                                                                                                   
    end for   
    rows = []
    for i in lines.indexes
        fields = lines[i].split(",")
        row = {}
        for j in headers.indexes
            if fields.hasIndex(j) then
                row[headers[j]] = fields[j].trim
            else
                row[headers[j]] = ""
            end if
        end for
        rows.push row
    end for
    return rows
end function
```
  Usage:
```
data = ["name, age, city", "Alice, 30, Denver", "Bob,25,Portland"]
rows = parseCSV(data)
for row in rows
    print row.name + " from " + row.city + " is " + row.age
end for
// Alice from Denver is 30
// Bob from Portland is 25
```
Key points:
- `lines.pull` removes the first element (index 0) from `lines` and returns it
- `.trim` strips whitespace around each header and field
- The `hasIndex` check handles rows with fewer fields than headers, defaulting to ""
- `.indexes` is an idiomatic way to loop over all indexes of a list or string
- Returned maps support dot notation, so `row.name` works as long as headers are valid identifiers

## Graph BFS

**User:** Write a MiniScript function to do breadth-first search over a graph.

**Assistant:**
```
bfs = function(graph, start, goal)
    queue = [[start, [start]]]  // [node, pathToNode]
    visited = {}
    visited[start] = 1
    while queue.len > 0
        entry = queue.pull
        node = entry[0]
        path = entry[1]
        if node == goal then return path
        if not graph.hasIndex(node) then continue
        for neighbor in graph[node]
            if not visited.hasIndex(neighbor) then
                visited.push neighbor
                newPath = path + [neighbor]
                queue.push [neighbor, newPath]
            end if
        end for
    end while
    return null
end function
```
Usage:
```
graph = {}
graph["A"] = ["B", "C"]
graph["B"] = ["A", "D", "E"]
graph["C"] = ["A", "F"]
graph["D"] = ["B"]
graph["E"] = ["B", "F"]
graph["F"] = ["C", "E"]

path = bfs(graph, "A", "F")
print path  // ["A", "C", "F"]
```
Key points:
- `queue.pull` removes and returns the first element — used as a FIFO queue
- `visited` is a map used as a set, adding items with `push` and checking with `hasIndex`
- Returns `null` if no path exists, or the shortest path as a list of nodes

# Code Fixing

## Index error caused by incorrect use of `range`

**User:** The following code generates an error.  What's wrong with it?                                                                                
```                                                                                                                                      
s = "Hello"
for i in range(0, s.len)
    print s[i]
end for
```

**Assistant:** The issue is that `range` in MiniScript includes the end value. So `range(0, s.len)` produces `[0, 1, 2, 3, 4, 5]`, and `s[5]` is out of bounds for a 5-character string (valid indices are 0–4).
                                                                                                                               
Fix:
```
s = "Hello"
for i in range(0, s.len - 1, 1)
    print s[i]
end for
```
The explicit step 1 ensures that if s is empty (`s.len - 1` == `-1`), the range returns `[]` rather than counting down `[0, -1]`.

Or more idiomatically, just iterate the string directly:
```
s = "Hello"
for ch in s
    print ch
end for
```

## Python-style class syntax

**User:** Why doesn't this code work?
```
class Dog:
    def speak(self):
        print "Woof!"
    end function
end class

d = new Dog
d.speak
```

**Assistant:** MiniScript uses prototype-based OOP, not class-based like Python. There's no `class` keyword, no `def`, and no explicit `self` parameter. Fix:
```
Dog = {}                                                                                                                                     
Dog.speak = function
    print "Woof!"                                                                                                                            
end function                                              

d = new Dog
d.speak
```
Key differences:
- Objects are just maps (`{}`)
- Methods are assigned as properties
- `self` is automatically available inside methods — don't declare it as a parameter
- `new` creates an instance with `__isa` pointing to the prototype

## Using `elif` instead of `else if`

**User:** This code gives me a compiler error and I can't figure out why.
```
x = 15
if x > 20 then
    print "big"
elif x > 10 then
    print "medium"
else
    print "small"
end if
```

**Assistant:** The keyword for additional conditions in MiniScript is else if, not elif (that's Python). Fix:
```
  x = 15                                                                                                                                       
  if x > 20 then
      print "big"                                                                                                                              
  else if x > 10 then                                       
      print "medium"
  else
      print "small"
  end if
```

## Assigning to a global variable without `globals`

**User:** Why does this print `0` instead of `5`?
```
count = 0

addToCount = function(n)
    count = count + n
end function

addToCount 5
print count
```

**Assistant:** The issue is scoping. Inside the function, `count = count + n` reads `count` from the outer scope, but the assignment creates a new local variable called `count`. The outer `count` is never modified.
                                                                                                                                               
To update the outer variable, use `outer` or `globals`:
```
count = 0

addToCount = function(n)
    outer.count = count + n
end function

addToCount 5
print count
```
This prints 5. The rule: unqualified assignments always target local scope. Use `outer.varName` or `globals.varName` to write to other scopes.

# Translation

## Binary search (Python)

**User:** Translate this Python program into MiniScript:
```
def binary_search(l, value):
    low = 0
    high = len(l)-1
    while low <= high: 
        mid = (low+high)//2
        if l[mid] > value: high = mid-1
        elif l[mid] < value: low = mid+1
        else: return mid
    return -1
myList = list(range(5,25))
print(binary_search(myList, 7)) # 2
print(binary_search(myList, 42)) # -1
```

**Assistant:**
```
binarySearch = function(l, value)
    low = 0
    high = l.len - 1                                                                                                                         
    while low <= high
        mid = floor((low + high) / 2)                                                                                                        
        if l[mid] > value then                            
            high = mid - 1
        else if l[mid] < value then
            low = mid + 1
        else
            return mid
        end if
    end while
    return -1
end function

myList = range(5, 24)
print binarySearch(myList, 7)   // 2
print binarySearch(myList, 42)  // -1
```

Key changes from Python:
- def → `function` / `end function`
- `len(l)` → `l.len` (though `len(l)` would also work, it's less idiomatic)
- `//` (integer division) → `floor(... / 2)`
- `elif` → `else if`
- `range(5,25)` → `range(5, 24)` because MiniScript's `range` is inclusive on both ends
- No colon after `while`/`if`/`else` — use `then` after `if`, and keyword delimiters for blocks

## FizzBuzz (Python)

**User:** Translate the following from Python into MiniScript:
```
for i in xrange(1, 101):
    if i % 15 == 0:
        print "FizzBuzz"
    elif i % 3 == 0:
        print "Fizz"
    elif i % 5 == 0:
        print "Buzz"
    else:
        print i
```

**Assistant:**
```
for i in range(1, 100)
    if i % 15 == 0 then
        print "FizzBuzz"
    else if i % 3 == 0 then
        print "Fizz"
    else if i % 5 == 0 then
        print "Buzz"
    else
        print i
    end if
end for
```
Key changes:
- `xrange(1, 101)` → `range(1, 100)` — MiniScript `range` is inclusive
- `elif` → `else if`
- Colons removed, `then` added after `if`/`else if` conditions
- Block delimiters `end if` / `end for` instead of indentation


## LCM (Lua)

**User:** Translate this program from Lua to MiniScript:
```
function gcd( m, n )
    while n ~= 0 do
        local q = m
        m = n
        n = q % n
    end
    return m
end

function lcm( m, n )
    return ( m ~= 0 and n ~= 0 ) and m * n / gcd( m, n ) or 0
end

print( lcm(12,18) ) -- 36
```

**Assistant:**
```
gcd = function(m, n)
    while n
        q = m                                                                                                                                
        m = n
        n = q % n                                                                                                                            
    end while                                             
    return m
end function

lcm = function(m, n)
    if m and n then return m * n / gcd(m, n)
	return 0
end function

print lcm(12, 18) // 36
```
Key changes from Lua:
- `function name(...)` → `name = function(...)`/`end function`
- `n ~= 0` → `n` — nonzero numbers are considered `true` in MiniScript
- `while ... do` / `end` → `while` / `end while`
- `local` keyword not needed — variables are local by default in MiniScript
- Lua's ternary idiom `(a and b) and x or y` → explicit `if` statements
- No parentheses needed on `print` statements
- `--` comment marker → `//` in MiniScript

## Function reference (Lua)

**User:** Convert the following Lua program into MiniScript.                                                                                           
```                                                                                                                                      
function sayHi ()                                                                                                                            
    print("Hi!")                                                                                                                             
end                                                                                                                                          
                                                                                                                                           
function rep (func, times)                                                                                                                   
    for count = 1, times do                                                                                                                  
        func()                                                                                                                               
    end                                                                                                                                      
end                                                                                                                                          
                                                                                                                                           
rep(sayHi, 4)                                                                                                                                
```

**Assistant:**
```
sayHi = function                                                                                                                             
    print "Hi!"                                                                                                                              
end function                                                                                                                                 
                                                                                                                                           
rep = function(func, times)                                                                                                                  
    for count in range(1, times)                                                                                                             
        func
    end for
end function

rep @sayHi, 4
```
Key changes from Lua:
- `function name(...)` / `end` → `name = function(...)` / `end function`
- `for count = 1, times do` / `end` → `for count in range(1, times)` / `end for`
- `func()` → `func` — in MiniScript, bare reference to a function invokes it
- `rep(sayHi, 4)` → `rep @sayHi, 4` — use `@` to pass a function reference without invoking it, and no parens needed on a statement-level call

## Rot-13 (C#)

**User:** Convert the following program from C# to MiniScript: 
```
using System;
using System.Linq;

class Program {
    private static char shift(char c) {
        return c.ToString().ToLower().First() switch {
            >= 'a' and <= 'm' => (char)(c + 13),
            >= 'n' and <= 'z' => (char)(c - 13),
            var _ => c
        };
    }

    static string Rot13(string s) => new string(s.Select(c => shift(c)).ToArray());

    static void Main(string[] args) {
        string test = "Hello world!";
        Console.WriteLine(Rot13(test));
    }
}
```

**Assistant:**
```
shift = function(c)
	lower = c.lower
	if lower >= "a" and lower <= "m" then                                                                                                    
		return char(c.code + 13)
	else if lower >= "n" and lower <= "z" then                                                                                               
		return char(c.code - 13)                          
	else
		return c
	end if
end function

rot13 = function(s)
	result = ""
	for c in s
		result += shift(c)
	end for
	return result
end function

test = "Hello world!"
print rot13(test)
```
Key changes from C#:
- `c.ToString().ToLower().First()` → `c.lower` — iterating a string already gives single characters
- `(char)(c + 13)` → `char(c.code + 13)` — `.code` gets the Unicode value, `char()` converts back
- String comparison works directly in MiniScript (`"a" <= "m"`)
- `s.Select(c => shift(c))` → simple `for c in s` loop building a result string
- No classes, namespaces, or type declarations needed

## GCD (Pseudocode)

**User:** Convert this pseudocode to MiniScript.
```
function gcd(a, b)
    while b != 0
        t := b
        b := a mod b
        a := t
    return a
```

**Assistant:**
```
gcd = function(a, b)
    while b != 0
        t = b
        b = a % b
        a = t
    end while
    return a
end function

print gcd(48, 18)  // 6
```

Key translations:

- `gcd = function(a, b)` rather than `function gcd(a, b)` — functions are first-class values assigned to variables
- `=` instead of `:=` for assignment
- `%` instead of `mod` for modulo
- `end while` and `end function` to close blocks — every `while` needs a matching `end while`, and every `function` needs `end function`

## Recursive GCD (Pseudocode)

**User:** Convert this pseudocode to MiniScript.
```
function gcd(a, b)
    if b = 0
        return a
    else
        return gcd(b, a mod b)
```

**Assistant:**
```
gcd = function(a, b)
    if b == 0 then return a
    return gcd(b, a % b)
end function
```

Key translations from the pseudocode:

- `==` for equality testing (single `=` is assignment in MiniScript)
- `%` instead of `mod` for modulo
- `if`/`then` — MiniScript conditionals require `then` after the condition; for a single-line `if`, you can put the result on the same line and skip `end if`
- No `else` needed since the `if` branch returns; the final `return` only executes when `b != 0`
- Recursion works directly — `gcd(b, a % b)` calls the function itself

## Binary Search (Pseudocode)

**User:** Implement the following algorithm in MiniScript.

The inputs are the array, which we call `array`; the number `n` of elements in array; and `target`, the number being searched for. The output is the index in `array` of `target`:

1. Let min = 0 and max = n-1.
2. Compute guess as the average of max and min, rounded down (so that it is an integer).
3. If array[guess] equals target, then stop. You found it! Return guess.
4. If the guess was too low, that is, array[guess] < target, then set min = guess + 1.
5. Otherwise, the guess was too high. Set max = guess - 1.
6. Go back to step 2.

**Assistant:** Here's a direct implementation of that binary search algorithm:

```
binarySearch = function(array, n, target)
    min = 0
    max = n - 1
    while min <= max
        guess = floor((max + min) / 2)
        if array[guess] == target then return guess
        if array[guess] < target then
            min = guess + 1
        else
            max = guess - 1
        end if
    end while
    return null
end function
```

The function follows the described steps exactly. `floor` rounds the average down to an integer (step 2). If the target is found, it returns the index immediately (step 3). If the guess is too low, `min` is adjusted up (step 4); if too high, `max` is adjusted down (step 5). The `while` loop handles step 6 (going back to step 2). It returns `null` if the target isn't in the array, which happens when `min` exceeds `max`.

Example usage:

```
data = [2, 3, 5, 7, 11, 13, 17, 19, 23]
print binarySearch(data, data.len, 13)   // prints 5
print binarySearch(data, data.len, 4)    // prints null
```

# Explanation

## Semiprime

**User:** Explain what this MiniScript function is doing.                                                                                              

```
isSemiprime = function(num)
    divisor = 2
    primes = 0
    while primes < 3 and num != 1
        if num % divisor == 0 then
            num = num / divisor
            primes += 1
        else
            divisor = divisor + 1
        end if
    end while
    return primes == 2
end function
```

**Assistant:** This function checks whether a number is a semiprime — a number that is the product of exactly two prime factors (e.g., 6 = 2×3, 9 = 3×3, 15 = 3×5).
                                                                       
How it works:
                                                                                                                                           
1. Starting with `divisor = 2`, it tries to divide num by the smallest possible factors
2. Each time `divisor` divides evenly, it divides `num` and increments `primes` (the prime factor count)
3. If divisor doesn't divide evenly, it tries the next one
4. The loop exits early if it finds 3 prime factors (can't be semiprime) or num is fully factored down to 1
5. Returns whether exactly 2 prime factors were found

Example: `isSemiprime(15)` → divides by 3 (primes=1, num=5), then by 5 (primes=2, num=1) → returns `1` (true).

## Levenshtein distance

**User:** Explain this code:
```
string.editDistance = function(s2)
	n = self.len
	m = s2.len
	if n == 0 then return m
	if m == 0 then return n
	
	s1chars = self.split("")
	s2chars = s2.split("")
	d = range(0, m)	
	lastCost = 0
	
	for i in range(1, n)
		s1char = s1chars[i-1]
		lastCost = i
		jMinus1 = 0
		for j in range(1, m)
			if s1char == s2chars[jMinus1] then cost = 0 else cost = 1
			
			// set nextCost to the minimum of the following three possibilities:
			a = d[j] + 1
			b = lastCost + 1
			c = cost + d[jMinus1]
			
			if a < b then
				if c < a then nextCost = c else nextCost = a
			else
				if c < b then nextCost = c else nextCost = b
			end if
			
			d[jMinus1] = lastCost
			lastCost = nextCost
			jMinus1 = j
		end for
		d[m] = lastCost
	end for
	
	return nextCost
end function
```

**Assistant:**
This adds an edit distance (Levenshtein distance) method to the `string` type. It computes the minimum number of single-character edits (insertions, deletions, or substitutions) needed to transform one string into another.
                                                                                                                                               
For example, `"kitten".editDistance("sitting")` returns 3.
                                                                                                                                               
How it works:

This is the classic Wagner-Fischer dynamic programming algorithm, optimized to use a single 1D array d instead of a full 2D matrix.

1. Base cases: If either string is empty, the distance is the length of the other string.
2. Setup: `d` is initialized to `range(0, m)` — representing the cost of inserting each character of `s2` from nothing.
3. Main loop: For each character `i` in `self` (the first string):
  - It walks through each character `j` in `s2`
  - At each step, it computes the minimum cost from three operations:
    - `a` = `d[j] + 1` — deletion (cost from the row above + 1)
    - `b` = `lastCost + 1` — insertion (cost from the left + 1)
    - `c` = `cost + d[jMinus1]` — substitution (diagonal cost + 0 if chars match, 1 if not)
  - The minimum of `a`, `b`, `c` becomes `nextCost`
  - `d` is updated in-place as it goes, with `lastCost` tracking the previous column's value
4. Result: The final `nextCost` is the edit distance.

MiniScript-specific note: By assigning this to `string.editDistance`, it becomes a method available on all strings, since `string` is the prototype for all string values. The string it's called on is accessed via `self`.

## Shoelace formula for polygon area

**User:** What's going on in this code?
```
shoelace = function(vertices)
    sum = 0
    points = vertices.len
    
    for i in range(0,points-2)
        sum = sum + vertices[i][0]*vertices[i+1][1]
    end for
    sum = sum + vertices[points-1][0]*vertices[0][1]
    
    for i in range(points-1,1)
        sum = sum - vertices[i][0]*vertices[i-1][1]
    end for
    sum = sum - vertices[0][0]*vertices[points-1][1]
    
    return abs(sum)/2
end function

verts = [[3,4],[5,11],[12,8],[9,5],[5,6]]
print shoelace(verts)
```

**Assistant:** This implements the Shoelace formula (also called Gauss's area formula) to calculate the area of a polygon given its vertices.

How it works:                                                                                                                                

Given a list of 2D vertices like `[x, y]`, the formula computes the area by cross-multiplying coordinates:                                     
                                                        
1. First loop — sums the "forward" cross products: each vertex's x times the next vertex's y (`x₀y₁ + x₁y₂ + x₂y₃ + ...`)
2. Wrapping term — adds the last vertex's x times the first vertex's y to close the polygon
3. Second loop — subtracts the "backward" cross products: each vertex's x times the previous vertex's y (`x₁y₀ + x₂y₁ + x₃y₂ + ...`), going
from the last vertex down to index 1
4. Wrapping term — subtracts the first vertex's x times the last vertex's y
5. Result — `abs(sum) / 2` gives the polygon's area (the `abs` ensures a positive result regardless of vertex winding order)

For the given pentagon with vertices `[3,4], [5,11], [12,8], [9,5], [5,6]`, it prints 30.

Note: There's a subtle bug risk — the second loop uses range(points-1, 1). Since MiniScript's range auto-descends, this correctly counts down. But if there were fewer than 2 vertices, it could behave unexpectedly.

# API/Documentation Questions

## Map iteration

**User:** How do I iterate over a map in MiniScript?                                                                                                   
                                             
**Assistant:** In MiniScript, iterate over a map using a `for` loop:                                                                                          
                                                                                                                                         
m = {"a": 1, "b": 2, "c": 3}                                                                                                                 
for kv in m
    print kv.key + ": " + kv.value                                                                                                           
end for                                                                                                                                    

The loop variable (`kv` in this example) is a mini-map with `.key` and `.value` properties for each entry.

## Repeating `n` times

**User:** How do I repeat some code `n` times?

**Assistant:** You can use a `for` loop with a `range` from `1` to `n`:
```
for i in range(1, n, 1):
    print "Iteration " + i
end for
```
Alterantively, if you want to start counting at zero, you could use `range(0, n-1, 1)`.

The explicit step `1` (third parameter to `range`) ensures that it always counts up or returns an empty list; without it, `range(1, n)` would return `[1, 0]` when `n` is `0`.

# Style & Idioms
## Dice-rolling example

**User:** How can I make the following MiniScript code more idiomatic?
```
rollDice = function(diceStr)
	// parse the string
	result = 0;
	modifier = 0;
	plusPos = diceStr.indexOf("+");
	minusPos = diceStr.indexOf("-");
	if (plusPos != null) then
		modifier = (diceStr[(plusPos + 1):]).val;
		diceStr = (diceStr[:plusPos]);
	else if (minusPos != null) then
		modifier = -(diceStr[(minusPos + 1):]).val;
		diceStr = (diceStr[:(minusPos)]);
	end if
	dPos = diceStr.indexOf("d");
	if (dPos == null) then
		return(null);
	end if
	numDice = (diceStr[:(dPos)]).val;
	numSides = (diceStr[(dPos + 1):]).val;
	if (numDice == 0 or numSides == 0) then
		return(null);
	end if
	result = {};
	result["rolls"] = [];
	result["total"] = modifier;
	for i in range(0, (numDice - 1))
		roll = floor(rnd * numSides) + 1;
		result["rolls"].push(roll);
		result["total"] = result["total"] + roll
	end for
	return(result);
end function

print(rollDice("3d6+1"));
```

**Assistant:** Here is a cleaned-up version:

```
rollDice = function(diceStr)
	modifier = 0
	plusPos = diceStr.indexOf("+")
	minusPos = diceStr.indexOf("-")
	if plusPos != null then
		modifier = diceStr[plusPos+1:].val
		diceStr = diceStr[:plusPos]
	else if minusPos != null then
		modifier = -diceStr[minusPos+1:].val
		diceStr = diceStr[:minusPos]
	end if
	dPos = diceStr.indexOf("d")
	if dPos == null then return null
	numDice = diceStr[:dPos].val
	numSides = diceStr[dPos+1:].val
	if numDice == 0 or numSides == 0 then return null
	result = {}
	result.rolls = []
	result.total = modifier
	for i in range(1, numDice)
		roll = ceil(rnd * numSides)
		result.rolls.push roll
		result.total += roll
	end for
	return result
end function

print rollDice("3d6+1")
```

Summary of changes:

- Removed semicolons — they're used only to separate multiple statements on a line, and are unnecessary noise at the end of a line
- Removed parentheses from `if` conditions, `return`, `print`, and `.push` — parentheses aren't needed on statement-level calls or conditionals
- Removed redundant parentheses around slice expressions like `(diceStr[(plusPos + 1):])` → `diceStr[plusPos+1:]`
- Dot notation for map keys: `result.rolls` instead of `result["rolls"]`
- `range(1, numDice)` - more readable/idiomatic, and doesn't affect the behavior since the loop variable isn't used
- Removed unused `result = 0` at the top (it was immediately overwritten)

# Questions from _Learn to Code in 30 Days_

## Variables and assignment

**User:** How do variables work in MiniScript? Do I need to declare them with a type?

**Assistant:** Here's a quick example showing global and local variables:

```
demo = function
    g = "local value"       // creates a NEW local g
    print g                 // local value
    print globals.g         // global value
    globals.g = "changed"
end function

g = "global value"
demo
print g                     // changed
```

There are six data types in MiniScript: number, string, list, map, function, and null. You can check a value's type at runtime if needed:

```
x = 3.14
if x isa number then print "It's a number!"
```

In short, there are no type declarations, no `var` or `let` keywords, and no type annotations. Just pick a name and assign a value.

## Updating a variable with its own value

**User:** How do I increment a variable or add to its existing value in MiniScript?

**Assistant:** MiniScript supports compound assignment operators, so you don't need to write out the variable name twice. You can use `+=` to add to an existing value, along with similar operators for other arithmetic operations.

```
x = 10
x += 1       // x is now 11
x += 5       // x is now 16
x -= 3       // x is now 13
x *= 2       // x is now 26
x /= 4       // x is now 6.5
```

The `+=` operator also works with strings for concatenation:

```
greeting = "Hello"
greeting += ", world!"
print greeting   // Hello, world!
```

And it works with lists using `push` behavior when combined with `+`:

```
myList = [1, 2, 3]
myList += [4, 5]
print myList   // [1, 2, 3, 4, 5]
```

The long form `x = x + 1` also works, but `x += 1` is preferred as it is cleaner and more idiomatic. Note that there are no `++` or `--` operators in MiniScript; use `x += 1` and `x -= 1` instead.

## Comments in MiniScript

**User:** How do I add comments to my MiniScript code?

**Assistant:** MiniScript uses `//` for comments. Everything from `//` to the end of the line is ignored by the compiler. There is no block comment syntax (like `/* */` in some other languages), so each comment line needs its own `//`.

Here are some examples:

```
// This is a full-line comment

x = 42  // This is an inline comment after a statement

// You can use comments to explain logic:
// Calculate the area of a circle
radius = 5
area = pi * radius ^ 2
print "Area: " + area

// Comments are handy for temporarily disabling code:
// print "This line won't run"
```

Since there are no multi-line block comments, if you need to comment out a larger section, just put `//` at the start of each line:

```
// This function is not ready yet:
// myFunc = function(x)
//     return x * 2
// end function
```

## Getting user input

**User:** How do I get input from the user in MiniScript?

**Assistant:** In most MiniScript environments, you can use the `input` function to prompt the user and get a string back:

```
name = input("What is your name? ")
print "Hello, " + name + "!"
```

The `input` function takes an optional prompt string, displays it, waits for the user to type a line and press Enter, and returns what they typed as a string.

If you need a number from the user, convert the result with `val`:

```
s = input("Enter a number: ")
n = s.val
print "Double that is: " + n * 2
```

If the user types something that isn't a valid number, `val` returns 0. You can check for this if needed:

```
s = input("Enter a number: ")
if s.val == 0 and s != "0" then
    print "That's not a valid number."
else
    print "You entered: " + s.val
end if
```

Calling `input` with no argument works too — it just waits for input without displaying a prompt.

## Converting strings to numbers with `val`

**User:** I'm trying to add a number the user typed in, but MiniScript is concatenating strings instead of adding. What's going on?

**Assistant:** The `input` function in MiniScript always returns a string. So when you use the `+` operator on two strings, it concatenates them rather than adding them as numbers. You need to convert the input to a number using the `val` function.

Here is the problem in action:
```
x = input("Enter a number: ")
print x + 10
```
If you type 5, this prints `510` because `x` is the string `"5"`, and `"5" + 10` concatenates them.

The fix is to use `val` to convert the string to a number:
```
x = input("Enter a number: ").val
print x + 10
```
Now if you type 5, this correctly prints `15`.

You can also convert after the fact:
```
x = input("Enter a number: ")
print x.val + 10
```

The `val` function parses a string and returns its numeric value. If the string is not a valid number, `val` returns 0. This is the standard way to handle numeric user input in MiniScript.

## Comparison operators and boolean values

**User:** How do I compare numbers or strings in MiniScript?

**Assistant:** MiniScript supports six comparison operators:

- `==` (equal)
- `!=` (not equal)
- `<` (less than)
- `>` (greater than)
- `<=` (less than or equal)
- `>=` (greater than or equal)

These work on numbers, strings (compared alphabetically), and lists.
```
print 5 > 3       // 1 (true)
print 5 == 5      // 1 (true)
print 5 != 3      // 1 (true)
print "apple" < "banana"  // 1 (true, alphabetical order)
```

MiniScript has no separate boolean type. Instead, it uses numbers: `1` means true and `0` means false. The keywords `true` and `false` are just shortcuts for `1` and `0`:
```
print true       // 1
print false      // 0
print true == 1  // 1
```

You can combine comparisons with the logical operators `and`, `or`, and `not`:
```
x = 15
print x > 10 and x < 20  // 1 (true: x is between 10 and 20)
print x < 5 or x > 100   // 0 (false: neither condition is met)
print not (x == 15)       // 0 (false: x is 15, negated)
```

It's also possible to chain several comparisons in a row, in which case, each pair of operands is considered in turn.  This is often used for checking whether a number is within a civen range:
```
x = 15
print 10 <= x <= 20    // 1 (true: x is between 10 and 20, inclusive)
```

Since any nonzero number counts as true and zero counts as false, you can use numbers directly in conditions:
```
lives = 3
if lives then print "Still playing!"   // prints, because 3 is truthy
lives = 0
if not lives then print "Game over!"   // prints, because 0 is falsy
```

One thing to watch out for: `null` is not the same as `0`. A comparison like `null == 0` evaluates to `0` (false), and using `null` in a boolean context is falsy, but it's not a number.

## While loops

**User:** How do I write a `while` loop in MiniScript?

**Assistant:** A `while` loop in MiniScript repeats a block of code as long as a condition is true. The basic structure is:
```
while condition
    // code to repeat
end while
```

Here's a simple example that counts from 1 to 5:
```
i = 1
while i <= 5
    print i
    i += 1
end while
// 1
// 2
// 3
// 4
// 5
```

You can use `break` to exit the loop early, and `continue` to skip to the next iteration:
```
i = 0
while i < 10
    i += 1
    if i % 2 == 0 then continue
    if i > 7 then break
    print i
end while
// 1
// 3
// 5
// 7
```

A `while true` loop runs forever until explicitly broken out of, which is useful for input loops or game loops:
```
while true
    line = input("Enter a number (0 to quit): ")
    n = line.val
    if n == 0 then break
    print n + " squared is " + n^2
end while
```
Key points:
- The condition is checked before each iteration, so the body may execute zero times
- There are no parentheses around the condition (unlike C or Java)
- The block must be closed with `end while`
- `break` and `continue` work as you'd expect from other languages

## For loops and `range`

**User:** How do I write a `for` loop in MiniScript?

**Assistant:** A `for` loop in MiniScript iterates over a collection (list, string, or map), by assigning a _loop variable_ to each element of the collection in turn.

**Iterating over a list:**
```
fruits = ["apple", "banana", "cherry"]
for fruit in fruits
    print fruit
end for
```
This prints each element in the list. You can also iterate over a string (getting each character), or over a map (getting key-value pairs).

**Iterating over a map:**
```
ages = {"Alice": 30, "Bob": 25}
for kv in ages
    print kv.key + " is " + kv.value
end for
```
When iterating over a map, each iteration variable is a mini-map with `.key` and `.value` properties.

**Using `range` for numeric loops:**

The `range` function generates a list of numbers. It takes up to three arguments: `range(start, end, step)`, and is very commonly used with `for`.
```
for i in range(1, 5)
    print i
end for
// prints 1, 2, 3, 4, 5
```
Important: unlike Python, `range` in MiniScript is *inclusive* of the end value. So `range(1, 5)` gives `[1, 2, 3, 4, 5]`, not `[1, 2, 3, 4]`.

**With a step value:**
```
for i in range(0, 10, 2)
    print i
end for
// prints 0, 2, 4, 6, 8, 10
```

**Counting down:**

`range` auto-descends when the start is greater than the end:
```
for i in range(5, 1)
    print i
end for
// prints 5, 4, 3, 2, 1
```
However, when using computed bounds, it is best practice to include an explicit step to avoid surprises. For example, `range(0, n-1)` when `n` is 0 would produce `[0, -1]` instead of an empty list. Use `range(0, n-1, 1)` to ensure it returns `[]` when n is 0. Similarly, when counting down use `range(n-1, 0, -1)`.

**With just one argument:**

`range` with a single argument counts from 0 up to that value:
```
for i in range(3)
    print i
end for
// prints 0, 1, 2, 3
```
Note again that this is inclusive, so `range(3)` gives four values: 0, 1, 2, and 3.

## `range`

**User:** How does `range` work in MiniScript?

**Assistant:** The `range` function generates a list of numbers. It can take one, two, or three arguments: `range(end)`, `range(start, end)`, or `range(start, end, step)`.

**Two-argument form — inclusive end:**

Unlike Python, MiniScript's `range` includes the end value:
```
print range(1, 5)   // [1, 2, 3, 4, 5]
```

**Single-argument form:**

With one argument, `range` counts from 0 up to (and including) that value:
```
print range(3)   // [0, 1, 2, 3]
```
Note this produces four values, not three.

**Auto-descending behavior:**

When the start value is greater than the end value, `range` automatically counts down:
```
print range(5, 1)   // [5, 4, 3, 2, 1]
```

**Explicit step parameter:**

The optional third argument sets the step size:
```
print range(0, 10, 2)    // [0, 2, 4, 6, 8, 10]
print range(10, 0, -2)   // [10, 8, 6, 4, 2, 0]
```

**Common pitfall — auto-descend with computed bounds:**

The auto-descending behavior can cause bugs when bounds are computed. Consider `range(0, n-1)` intended to count from 0 up to the last index. When `n` is 0, this becomes `range(0, -1)`, which auto-descends and returns `[0, -1]` instead of an empty list. The fix is to include an explicit step:
```
// Bad — returns [0, -1] when n is 0:
print range(0, n - 1)

// Good — returns [] when n is 0:
print range(0, n - 1, 1)
```
Similarly, when counting down with computed bounds, use an explicit step of -1 to avoid accidentally counting up:
```
range(n - 1, 0, -1)
```
As a rule of thumb: whenever either bound is a computed value, include an explicit step.

## Nested loops

**User:** Can I nest loops inside each other in MiniScript? Can you show me an example?

**Assistant:** Yes, you can absolutely nest loops inside each other in MiniScript. There is no limit to how deeply you can nest them, and you can mix loop types freely (e.g., a `for` loop inside a `while` loop, or vice versa).

Here is an example that prints a multiplication table using nested `for` loops:

```
for row in range(1, 5)
    line = ""
    for col in range(1, 5)
        product = row * col
        line += str(product) + char(9)  // char(9) is tab
    end for
    print line
end for
```

Output:
```
1	2	3	4	5
2	4	6	8	10
3	6	9	12	15
4	8	12	16	20
5	10	15	20	25
```

You can also nest different loop types. Here is an example that uses a `for` loop with a `while` loop inside it:

```
for word in ["cat", "do", "be"]
    result = word
    while result.len < 6
        result += word
    end while
    print result
end for
```

Output:
```
catcat
dododo
bebebe
```

Each inner loop runs to completion for every single iteration of the outer loop. The `break` and `continue` keywords apply only to the innermost loop they appear in, so you can control each loop independently.

## If/then/else

**User:** How do I write conditional statements in MiniScript?

**Assistant:** MiniScript uses `if`/`then`/`else if`/`else`/`end if` for conditional statements.

**Basic if/then:**
```
x = 10
if x > 5 then print "x is big"
```
When the body is short, you can put it on the same line after `then`.

**Multi-line if block:**
```
x = 10
if x > 5 then
    print "x is greater than 5"
    print "that's pretty big"
end if
```
When the body is more than one statement, put it on subsequent lines and close the block with `end if`.

**if/else:**
```
age = 15
if age >= 18 then
    print "You can vote."
else
    print "Too young to vote."
end if
```

**if/else if/else:**
```
score = 85
if score >= 90 then
    grade = "A"
else if score >= 80 then
    grade = "B"
else if score >= 70 then
    grade = "C"
else
    grade = "F"
end if
print "Your grade: " + grade
```
Note that it's `else if` (two words), not `elseif` or `elif`.

**Single-line form:**
```
x = 42
if x > 0 then print "positive" else print "non-positive"
```
This works for simple cases where each branch is just one statement.

Conditions use standard comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) and can be combined with `and`, `or`, and `not`:
```
temp = 72
humid = 40
if temp > 60 and temp < 80 and humid < 60 then
    print "Nice weather!"
end if
```

A few things to note:
- MiniScript has no separate boolean type; `true` is just `1` and `false` is `0`
- Any nonzero number is truthy; `0`, `""` (empty string), and `null` are falsy
- Parentheses around the condition are not needed (and are discouraged)

## Single-line `if` statements

**User:** Can I put an `if` statement on a single line in MiniScript?

**Assistant:** Yes! MiniScript supports single-line `if` statements. Just put the `then` clause on the same line as the `if`, and skip the `end if`:

```
x = 10
if x > 5 then print "big"
```

You can also include an `else` on the same line:

```
if x > 5 then print "big" else print "small"
```

This works for any single statement after `then` (and after `else`). You only need `end if` when the body spans multiple lines:

```
// Multi-line form (needs end if)
if x > 5 then
    print "big"
    print "very big indeed"
end if
```

The single-line form is handy for quick guards and early returns:

```
myFunc = function(n)
    if n == null then return 0
    return n * 2
end function
```

The key rule is: if the statement after `then` is on the **same line**, no `end if` is needed. If it's on the **next line**, you must close the block with `end if`.

## `break` and `continue`

**User:** How do I exit a loop early, or skip to the next iteration in MiniScript?

**Assistant:** MiniScript supports both `break` and `continue` for controlling loop execution.

Use `break` to exit a loop early:

```
for i in range(1, 100)
    if i > 5 then break
    print i
end for
// prints 1 through 5, then exits the loop
```

Use `continue` to skip the rest of the current iteration and move on to the next one:

```
for i in range(1, 10)
    if i % 2 == 0 then continue
    print i
end for
// prints only odd numbers: 1, 3, 5, 7, 9
```

Both work with `while` loops too:

```
while true
    line = input("Enter something (or 'quit'): ")
    if line == "quit" then break
    if line == "" then continue
    print "You said: " + line
end while
```

Note that `break` and `continue` apply to the innermost loop only. If you have nested loops and need to exit an outer loop, you can set a flag variable and check it after the inner loop:

```
done = false
for row in range(0, 9)
    for col in range(0, 9)
        if grid[row][col] == target then
            print "Found at " + row + "," + col
            done = true
            break
        end if
    end for
    if done then break
end for
```

## Creating and accessing lists

**User:** How do I create a list or array in MiniScript?

**Assistant:** In MiniScript, you create a list using square brackets, and access elements by index (0-based). Negative indices count from the end.

```
// Create a list
myList = [10, 20, 30, 40, 50]

// Access elements by index
print myList[0]    // 10 (first element)
print myList[2]    // 30 (third element)
print myList[-1]   // 50 (last element)
print myList[-2]   // 40 (second to last)
```

You can also create an empty list and add elements to it:

```
myList = []
myList.push "apple"
myList.push "banana"
myList.push "cherry"
print myList        // ["apple", "banana", "cherry"]
print myList[1]     // banana
```

Lists support slicing to get a sublist:

```
nums = [10, 20, 30, 40, 50]
print nums[1:3]    // [20, 30] (index 1 up to but not including 3)
print nums[2:]     // [30, 40, 50] (from index 2 to end)
print nums[:3]     // [10, 20, 30] (from start up to index 3)
print nums[-2:]    // [40, 50] (last 2 elements)
```

Lists can hold any mix of types, including other lists:

```
mixed = [1, "hello", [2, 3], null]
print mixed[1]       // hello
print mixed[2][0]    // 2
```

Useful list methods include `len` to get the size, `indexOf` to find an element, and `hasIndex` to check whether an index is valid:

```
colors = ["red", "green", "blue"]
print colors.len           // 3
print colors.indexOf("green")  // 1
print colors.hasIndex(5)   // 0 (false)
```

## Negative indexing

**User:** What does a negative index do on a list or string in MiniScript?

**Assistant:** In MiniScript, a negative index counts backward from the end of a list or string. Index `-1` refers to the last element, `-2` to the second-to-last, and so on. This works for both single-element access and slicing.

**With lists:**

```
myList = ["a", "b", "c", "d", "e"]
print myList[-1]    // e
print myList[-2]    // d
print myList[-3:]   // ["c", "d", "e"]  (last 3 elements)
print myList[1:-1]  // ["b", "c", "d"]  (from index 1 up to but not including the last)
```

**With strings:**

```
s = "Hello"
print s[-1]     // o
print s[-2]     // l
print s[-3:]    // llo  (last 3 characters)
print s[1:-1]   // ell  (from index 1 up to but not including the last)
```

This is a convenient way to access the end of a sequence without needing to know its length. Instead of writing `myList[myList.len - 1]`, you can simply write `myList[-1]`.

**User:** How do I count backwards into a list or string in MiniScript?

**Assistant:** Use negative indices to count backwards from the end. Index `-1` refers to the last element, `-2` to the second-to-last, and so on.

For lists:
```
nums = [10, 20, 30, 40, 50]
print nums[-1]   // 50 (last element)
print nums[-2]   // 40 (second to last)
print nums[-3]   // 30
```

For strings:
```
s = "Hello"
print s[-1]      // "o" (last character)
print s[-2]      // "l"
```

Negative indices also work with slicing:
```
nums = [10, 20, 30, 40, 50]
print nums[-3:]    // [30, 40, 50] (last 3 elements)
print nums[-3:-1]  // [30, 40] (from third-to-last up to but not including last)

s = "Hello"
print s[-3:]       // "llo" (last 3 characters)
```

Any place you use a positive index, you can substitute a negative one to count from the end instead.

## List methods: push, pop, pull, insert, remove

**User:** What methods are available for adding and removing elements from a list in MiniScript?

**Assistant:** MiniScript provides several methods for adding and removing elements from a list:

**Adding elements:**

- `push` — adds an element to the end of the list
- `insert` — inserts an element at a specific index position

```
myList = [1, 2, 3]

myList.push 4
print myList    // [1, 2, 3, 4]

myList.insert 0, "first"
print myList    // ["first", 1, 2, 3, 4]

myList.insert 2, "middle"
print myList    // ["first", 1, "middle", 2, 3, 4]
```

You can also use the `+` operator to concatenate two lists, which returns a new list rather than modifying the original:

```
a = [1, 2]
b = [3, 4]
c = a + b
print c    // [1, 2, 3, 4]
```

**Removing elements:**

- `pop` — removes and returns the last element
- `pull` — removes and returns the first element
- `remove` — removes the element at a specific index

```
myList = ["a", "b", "c", "d", "e"]

last = myList.pop
print last      // e
print myList    // ["a", "b", "c", "d"]

first = myList.pull
print first     // a
print myList    // ["b", "c", "d"]

myList.remove 1
print myList    // ["b", "d"]
```

Note that `remove` takes an index, not a value. To remove by value, first find the index with `indexOf`:

```
myList = ["apple", "banana", "cherry"]
idx = myList.indexOf("banana")
if idx != null then myList.remove idx
print myList    // ["apple", "cherry"]
```

## Immutable strings

**User:** How do I modify a string in MiniScript?

**Assistant:** Strings in MiniScript are **immutable value types**. You cannot change a character in place — any "modification" actually creates a new string. Here are the main techniques.

**Using `replace`:**
```
s = "Hello World"
s = s.replace("World", "MiniScript")
print s  // Hello MiniScript
```

**Using slicing and concatenation:**
```
s = "Hello!"
// Change character at index 2 from "l" to "L"
s = s[:2] + "L" + s[3:]
print s  // HeLlo!
```

**Using `remove` and `insert`:**
```
s = "cat"
s = s.remove("a")
print s  // ct

s = "Hllo"
s = s.insert(1, "e")
print s  // Hello
```

**Building up a string piece by piece:**
```
result = ""
for ch in "Hello"
    if ch == "l" then result += "r" else result += ch
end for
print result  // Herro
```

The key concept is that none of these operations change the original string. Each one produces a new string, which you then assign back to the variable (or to a different variable).

## Slicing lists and strings

**User:** How does slicing work in MiniScript?

**Assistant:** Slicing extracts a portion of a list or string using the syntax `value[start:end]`, where `start` is the first index included and `end` is the first index excluded (i.e., the end index is exclusive, just like Python).

**Basic slicing:**
```
myList = ["a", "b", "c", "d", "e"]
print myList[1:3]   // ["b", "c"]

s = "Hello World"
print s[0:5]        // Hello
```

**Omitting start or end:**

You can omit the start index to slice from the beginning, or omit the end index to slice to the end:
```
myList = [10, 20, 30, 40, 50]
print myList[:3]    // [10, 20, 30]
print myList[2:]    // [30, 40, 50]

s = "Hello"
print s[:3]         // Hel
print s[3:]         // lo
```

**Negative indices in slices:**

Negative indices count from the end, where -1 is the last element:
```
myList = [10, 20, 30, 40, 50]
print myList[-3:]   // [30, 40, 50]
print myList[:-1]   // [10, 20, 30, 40]

s = "Hello"
print s[-3:]        // llo
```

**Making a shallow copy:**

Omit both start and end to get a shallow copy of a list:
```
original = [1, 2, 3]
copy = original[:]
copy.push 4
print original      // [1, 2, 3]
print copy          // [1, 2, 3, 4]
```

This works on strings too, though since strings are value types in MiniScript, copying them is less of a concern.

Key points:
- The start index is inclusive; the end index is exclusive
- Omit the start to slice from the beginning; omit the end to slice through the end
- Negative indices count from the end
- `[:]` creates a shallow copy of a list
- Slicing works the same way on both lists and strings

## Substrings

**User:** How do I get a substring of a larger string?

**Assistant:** Use the slice syntax `s[start:end]` to extract a substring. The `start` index is inclusive and the `end` index is exclusive (i.e., the character at `end` is not included).

**Basic substring extraction:**
```
s = "Hello, World!"
print s[0:5]        // Hello
print s[7:12]       // World
```

**Omitting start or end:**

Leave out the start index to begin from the start of the string, or leave out the end index to go through the end:
```
s = "Hello, World!"
print s[:5]         // Hello
print s[7:]         // World!
```

**Negative indices:**

Negative indices count from the end of the string, where -1 is the last character:
```
s = "Hello, World!"
print s[-6:]        // orld!
print s[-6:-1]      // orld
print s[:-1]        // Hello, World
```

**Getting a single character:**

Use a single index (no colon) to get one character:
```
s = "Hello"
print s[0]          // H
print s[-1]         // o
```

**Practical examples:**

```
// Get a file extension
filename = "photo.png"
dotPos = filename.indexOf(".")
ext = filename[dotPos + 1:]
print ext           // png

// Get the first N characters
s = "MiniScript is fun"
print s[:10]        // MiniScript

// Get the last 3 characters
s = "abcdef"
print s[-3:]        // def

// Extract a middle portion
line = "Name: Alice Smith"
print line[6:]      // Alice Smith
```

Note that strings in MiniScript are value types, so slicing always produces a new string without affecting the original.

## Sublists

**User:** How do I get a portion of a list, like just the first three elements?

**Assistant:** Use the slice syntax `list[start:end]`, where `start` is the index of the first element you want, and `end` is the index just past the last element you want. Both are optional.

To get the first three elements:
```
myList = ["a", "b", "c", "d", "e"]
print myList[:3]   // ["a", "b", "c"]
```

When you omit `start`, it defaults to 0 (the beginning). When you omit `end`, it defaults to the end of the list:
```
myList = [10, 20, 30, 40, 50]

print myList[1:3]   // [20, 30] — elements at index 1 and 2
print myList[:2]    // [10, 20] — first two elements
print myList[3:]    // [40, 50] — from index 3 to the end
print myList[:]     // [10, 20, 30, 40, 50] — shallow copy of the whole list
```

You can also use negative indices, which count from the end:
```
myList = ["a", "b", "c", "d", "e"]

print myList[-3:]    // ["c", "d", "e"] — last three elements
print myList[-2:]    // ["d", "e"] — last two elements
print myList[:-1]    // ["a", "b", "c", "d"] — everything except the last
```

A slice always returns a new list, so modifying the slice won't affect the original. This makes `myList[:]` a handy way to make a shallow copy of a list.

## Reference types vs value types (lists)

**User:** I assigned a list to a new variable and changed the new variable, but the original list changed too. Why?

**Assistant:** In MiniScript, lists and maps are **reference types**. When you assign a list to a new variable, you are not making a copy — both variables point to the same list in memory. So any change through one variable is visible through the other.

```
a = [1, 2, 3]
b = a           // b points to the SAME list as a
b.push 4
print a         // [1, 2, 3, 4]  -- a changed too!
```

To make an independent copy, use the slice operator `[:]`:
```
a = [1, 2, 3]
b = a[:]        // b is a SHALLOW COPY of a
b.push 4
print a         // [1, 2, 3]  -- a is unchanged
print b         // [1, 2, 3, 4]
```

Note that `[:]` makes a **shallow** copy. If your list contains other lists or maps, those inner objects are still shared:
```
a = [[1, 2], [3, 4]]
b = a[:]
b[0].push 99
print a[0]      // [1, 2, 99]  -- inner list is still shared
```

To avoid that, you would need to copy each element individually:
```
a = [[1, 2], [3, 4]]
b = []
for item in a
    b.push item[:]
end for
b[0].push 99
print a[0]      // [1, 2]  -- truly independent now
```

This same behavior applies to maps. Assigning a map to a new variable does not copy it; use the `+` operator with an empty map (`myMap + {}`) to make a shallow copy of a map.

## Copying a list

**User:** How do I make a copy of a list in MiniScript so I can modify it without affecting the original?

**Assistant:** In MiniScript, assigning a list to a new variable does **not** copy it — both variables refer to the same list. To get an independent copy, use the slice operator `[:]`.
```
original = [1, 2, 3, 4, 5]

// This does NOT make a copy -- both point to the same list:
notACopy = original
notACopy.push 6
print original  // [1, 2, 3, 4, 5, 6] -- original was changed!

// This DOES make a copy:
original = [1, 2, 3, 4, 5]
copy = original[:]
copy.push 99
print original  // [1, 2, 3, 4, 5] -- original is unaffected
print copy      // [1, 2, 3, 4, 5, 99]
```
The slice operator is typically used to get a smaller sublist, but if you omit both the start and the end index, it copies from the beginning to the end.  In other words, this `[:]` syntax creates a shallow copy of the list. This means the list itself is new, but if it contains other lists or maps, those inner elements are still shared references. If you need a deep copy (where nested structures are also independent), you need to copy each level manually:
```
deepCopy = function(lst)
    result = []
    for item in lst
        if item isa list then
            result.push deepCopy(item)
        else
            result.push item
        end if
    end for
    return result
end function

nested = [[1, 2], [3, 4]]
independent = deepCopy(nested)
independent[0].push 99
print nested       // [[1, 2], [3, 4]] -- unaffected
print independent  // [[1, 2, 99], [3, 4]]
```
A few things to note:
- `[:]` is the idiomatic way to shallow-copy a list in MiniScript
- For simple lists of numbers or strings, a shallow copy is all you need since those types are values, not references

## Creating and using maps

**User:** How do I create and use a map (dictionary) in MiniScript?

**Assistant:** Maps (sometimes called dictionaries) are one of MiniScript's core data types. You create them with curly braces and access values by key using bracket or dot notation.

**Creating a map:**
```
// Empty map
m = {}

// Map with initial key-value pairs
person = {"name": "Alice", "age": 30, "city": "Portland"}
```

**Accessing and setting values:**

You can read or write a value for a key by putting the key after the map reference in square brackets, like `person["name"]`.  When the key happens to be a valid MiniScript identifier (i.e. starts with a letter or underscore, and contains only letters, underscores, and numbers), then you can also use dot notation, as shown here:

```
print person["name"]    // Alice
print person.name       // Alice (dot notation shorthand)

person["email"] = "alice@example.com"  // add a new entry
person.age = 31                        // update an existing entry
```

**Checking for keys and removing entries:**
```
if person.hasIndex("email") then print "Has email"
person.remove "email"
```

**Iterating over a map:**
```
for kv in person
    print kv.key + ": " + kv.value
end for
// name: Alice
// age: 31
// city: Portland
```
You can also get keys and values separately:
```
print person.indexes   // ["name", "age", "city"]
print person.values    // ["Alice", 31, "Portland"]
```

**Other useful properties:**
```
print person.len       // 3 (number of key-value pairs)
```

Note that bracket notation (`m["key"]`) works with any string, while dot notation (`m.key`) only works when the key is a valid identifier. Use bracket notation when keys contain spaces or special characters, or when the key is stored in a variable:
```
key = "name"
print person[key]      // Alice
```

## Map dot syntax vs bracket syntax

**User:** What's the difference between `myMap.key` and `myMap["key"]` in MiniScript?

**Assistant:** In MiniScript, `myMap.key` and `myMap["key"]` are functionally identical — they both look up the value associated with the string key `"key"` in the map. Dot notation is simply a convenient shorthand for bracket notation.

```
m = {"name": "Alice", "age": 30}

print m.name       // Alice
print m["name"]    // Alice  (same thing)

m.score = 100
print m["score"]   // 100  (dot assignment works too)
```

The only difference is practical: dot notation only works with keys that are valid identifiers (letters, digits, and underscores, not starting with a digit). If your key contains spaces, punctuation, or starts with a number, you must use bracket notation:

```
m = {}
m["full name"] = "Bob Smith"   // works fine
// m.full name = "Bob Smith"   // would NOT work (space in key)

m["42"] = "answer"
// m.42 = "answer"            // would NOT work (starts with digit)
```

The other important difference is that bracket notation lets you use a variable or expression as the key, while dot notation always uses a literal name:

```
m = {"x": 10, "y": 20}

key = "x"
print m[key]    // 10  (looks up the value of key, which is "x")
print m.key     // null (looks for a literal key called "key")
```

In short: use dot notation for clean, readable code when your keys are simple identifiers and known at write time. Use bracket notation when keys are dynamic (stored in variables) or contain characters that are not valid in an identifier.

## Reference types vs value types (maps)

**User:** I assigned a map to a new variable and changed the new variable, but the original map changed too. What's going on?

**Assistant:** In MiniScript, maps (and lists) are **reference types**. When you assign a map to a new variable, you are not making a copy — both variables point to the same map in memory. Any change through one variable is visible through the other.

```
original = {"name": "Alice", "score": 10}
copy = original
copy.score = 99
print original.score  // 99 -- original changed too!
```

Both `original` and `copy` refer to the exact same map, so changing `copy.score` also changes `original.score`.

To make an independent copy, use the `+` operator with an empty map:
```
original = {"name": "Alice", "score": 10}
copy = original + {}
copy.score = 99
print original.score  // 10 -- original is unaffected
```

The expression `original + {}` creates a new map and merges all key-value pairs from `original` into it. After that, `copy` and `original` are separate maps, and changes to one do not affect the other.

The same principle applies to lists. Assigning a list to a new variable gives you two references to the same list. To copy a list, use the slice shorthand `original[:]`.

## Defining and calling functions

**User:** How do I define and call a function in MiniScript?

**Assistant:** In MiniScript, you define a function with the `function` keyword and close it with `end function`. You assign it to a variable, then call it by name.

**Basic function with no parameters:**

```
sayHello = function
    print "Hello!"
end function

sayHello
```

**Function with parameters:**

```
greet = function(name)
    print "Hello, " + name + "!"
end function

greet "Alice"
```

**Function with a default parameter value:**

```
greet = function(name="World")
    print "Hello, " + name + "!"
end function

greet           // prints: Hello, World!
greet "Bob"     // prints: Hello, Bob!
```

**Function that returns a value:**

```
square = function(x)
    return x * x
end function

print square(4)   // prints: 16
```

Note the parentheses rules: when calling a function as a standalone statement (not part of a larger expression), parentheses are optional and discouraged — so you write `greet "Alice"` rather than `greet("Alice")`. But when the function call is embedded in an larger statement, such as passing its result to `print`, you do need parentheses: `print square(4)`.

You can also store a reference to a function using `@` and call it later:

```
f = @square
print f(5)   // prints: 25
```

## Function parameters and default values

**User:** Can MiniScript functions have default parameter values?

**Assistant:** Yes! You specify default values right in the parameter list using `=`:

```
greet = function(name="World", greeting="Hello")
    print greeting + ", " + name + "!"
end function

greet                    // Hello, World!
greet "Alice"            // Hello, Alice!
greet "Bob", "Hi"        // Hi, Bob!
```

If a caller omits an argument, the parameter takes its default value. Parameters without defaults get `null` if not provided:

```
test = function(a, b=10)
    print "a=" + a + ", b=" + b
end function

test 5        // a=5, b=10
test 5, 20    // a=5, b=20
test          // a=, b=10
```

## The `return` statement

**User:** How do I return a value from a function in MiniScript?

**Assistant:** Use the `return` keyword to send a value back from a function:

```
square = function(x)
    return x * x
end function

print square(4)   // 16
```

You can return early from anywhere in the function:

```
safeDiv = function(a, b)
    if b == 0 then return null
    return a / b
end function

print safeDiv(10, 3)   // 3.333333
print safeDiv(10, 0)   // null
```

A function that doesn't explicitly `return` a value returns `null` by default:

```
sayHi = function
    print "Hi!"
end function

result = sayHi    // prints "Hi!"
print result      // null
```

You can return any type — numbers, strings, lists, maps, even other functions:

```
makePair = function(a, b)
    return [a, b]
end function

print makePair("x", 42)   // ["x", 42]
```

Note that `return` doesn't need parentheses — `return x * x` is preferred over `return(x * x)`.

## Variable scope

**User:** How does variable scope work in MiniScript?

**Assistant:** MiniScript has a straightforward scoping model built around three layers: local, outer, and global.

**Variables are local by default.** Any assignment to an unqualified name creates or updates a variable in the current local scope.

**Unqualified reads walk up the scope chain.** When you read a variable, MiniScript looks first in locals, then the enclosing (outer) scope, then globals:
```
x = 100
f = function
    print x   // finds x in outer scope; prints 100
end function
f
```

**Unqualified writes always target local scope.** Even if a variable exists in an outer scope, assigning to it without a qualifier creates a new local variable instead:
```
x = 100
f = function
    x = 42       // creates a NEW local x; does NOT change the outer x
end function
f
print x          // still 100
```

**Use `outer` or `globals` to write to other scopes:**
```
x = 100
f = function
    outer.x = 42     // modifies x in the enclosing scope
end function
f
print x              // now prints 42
```

To summarize: reads automatically search upward through scopes, but writes always stay local unless you explicitly say `outer.varName` or `globals.varName`.

## local, outer, and global

**User:** What's the difference between local, outer, and global variables?

**Assistant:** MiniScript has three scope levels: **local**, **outer**, and **globals**.

**Local scope (the default):**

When you assign a variable inside a function, it's local to that function by default:
```
demo = function
    x = 10          // x is local to demo
    print x         // 10
end function
demo
// x is not accessible out here
```

**Global scope (`globals`):**

Globals are variables defined at the top level of your program, outside any function. Inside a function, use `globals.` to read or write them explicitly:
```
score = 100    // global (defined at top level)

addPoints = function(n)
    globals.score += n
end function

addPoints 50
print score    // 150
```

Without `globals.`, the assignment `score += n` would create a new local variable instead of updating the global one.

**Outer scope (`outer`):**

`outer` refers to the scope of the *enclosing* function — useful when you have a function defined inside another function:
```
makeCounter = function
    count = 0
    f = function
        outer.count += 1
        return outer.count
    end function
    return @f
end function

counter = makeCounter
print counter   // 1
print counter   // 2
print counter   // 3
```

Here, the inner function `f` uses `outer.count` to access and modify `count` in `makeCounter`'s scope.

**Summary of the rules:**

- **Reading** an unqualified variable searches: local → outer → globals
- **Writing** an unqualified variable always targets the **local** scope
- Use `outer.varName` to write to the enclosing function's scope
- Use `globals.varName` to write to the top-level scope

## Prototype-based OOP

**User:** How do I create classes and objects in MiniScript?

**Assistant:** MiniScript uses **prototype-based** OOP, not class-based. There's no `class` keyword. Instead, you create a map, add properties and methods to it, then use `new` to create instances.

**Defining a "class" (prototype):**

```
Dog = {}
Dog.name = "unknown"
Dog.speak = function
    print self.name + " says Woof!"
end function
```

**Creating an instance:**

```
myDog = new Dog
myDog.name = "Rex"
myDog.speak   // Rex says Woof!
```

`new Dog` creates a new map whose `__isa` property points to `Dog`. This causes the instance to inherit all of `Dog`'s properties and methods. Setting a property on the instance doesn't affect the prototype.

**Inheritance:**

```
Animal = {}
Animal.name = "unknown"
Animal.speak = function
    print self.name + " makes a sound"
end function

Dog = new Animal
Dog.speak = function
    print self.name + " says Woof!"
end function

Cat = new Animal
Cat.speak = function
    print self.name + " says Meow!"
end function

rex = new Dog
rex.name = "Rex"
rex.speak      // Rex says Woof!

whiskers = new Cat
whiskers.name = "Whiskers"
whiskers.speak  // Whiskers says Meow!
```

Any lookup of a map entry (such as `whiskers.speak` above) looks first in that map, but if it's not found, then MiniScript walks the `__isa` chain until it either finds the given key, or throws a "Key Not Found" error.  This is how properties and methods are inherited, and can be overridden, in the class hierarchy.

Key points:
- "Classes" are just maps used as prototypes
- `new` creates an instance with `__isa` pointing to the prototype
- `self` is automatically available inside methods — don't declare it as a parameter
- Property lookup walks the `__isa` chain: instance → prototype → prototype's prototype → etc.
- There are no constructors — just set properties after `new`, or use a factory method

## The `new` operator and `__isa`

**User:** What does the `new` operator do in MiniScript?

**Assistant:** The `new` operator creates a new map and sets its `__isa` property to point to the given prototype. This establishes an inheritance relationship.

```
Animal = {}
Animal.name = "unknown"
Animal.speak = function
    print self.name + " makes a sound"
end function

dog = new Animal
print dog        // {"__isa": {...}}
print dog.name   // unknown (inherited from Animal)
```

**How `__isa` works:**

When you access a property on a map and it's not found, MiniScript follows the `__isa` chain to look it up in the prototype. It's like a "parent" pointer:

```
dog.name = "Rex"    // sets name on the instance
print dog.name      // Rex (found on instance, no need to check __isa)
dog.speak           // Rex makes a sound (speak found via __isa → Animal)
```

**Chain of inheritance:**

`__isa` chains can be multiple levels deep:

```
Animal = {}
Animal.legs = 4

Dog = new Animal
Dog.sound = "Woof"

myDog = new Dog
print myDog.sound   // Woof (from Dog)
print myDog.legs    // 4 (from Animal, via Dog.__isa)
```

The lookup chain is: `myDog` → `Dog` → `Animal`.

**Checking inheritance:**

You can use `isa` to check if an object inherits from a prototype:

```
print myDog isa Dog     // 1 (true)
print myDog isa Animal  // 1 (true)
print myDog isa map     // 1 (true — all objects are maps)
```

You can also inspect `__isa` directly: `print Dog.__isa == Animal` prints `1`.  (But be careful, this only checks the _immediate_ parent, not more distant ancestors.)

## Using `self` in methods

**User:** How do I access an object's own properties inside its methods in MiniScript?

**Assistant:** Use the `self` keyword. When a method is called via dot notation, MiniScript automatically sets `self` to refer to the object the method was called on. You do **not** declare `self` as a parameter — it's provided automatically.

```
Dog = {}
Dog.name = "unknown"
Dog.tricks = 0

Dog.describe = function
    print self.name + " knows " + self.tricks + " tricks"
end function

Dog.learnTrick = function
    self.tricks += 1
    print self.name + " learned a trick!"
end function

rex = new Dog
rex.name = "Rex"
rex.describe       // Rex knows 0 tricks
rex.learnTrick     // Rex learned a trick!
rex.describe       // Rex knows 1 tricks
```

Important: you must use `self.propertyName` to access the object's properties. A bare `name` inside a method would look for a local or global variable called `name`, not the object's property:

```
Dog.broken = function
    print name       // WRONG: looks for local/global variable "name"
    print self.name  // RIGHT: accesses this object's name property
end function
```

`self` also works for calling other methods on the same object:

```
Dog.greet = function
    self.describe           // call another method on the same object
    print "Nice to meet you!"
end function
```

## Accessing superclass properties

**User:** How do I access a property or method defined in some superclass?

**Assistant:** In most cases, you don't need to do anything special. MiniScript's prototype chain (`__isa`) automatically walks up the inheritance hierarchy when you access a property or call a method.

**Automatic lookup via `__isa`:**

When you access a property on a map and it isn't found directly on that map, MiniScript follows the `__isa` chain to look it up in the parent prototype, then the grandparent, and so on.

```
Shape = {}
Shape.color = "red"
Shape.describe = function
    print "A " + self.color + " shape"
end function

Circle = new Shape
Circle.radius = 10

c = new Circle
print c.color       // red (found via Circle.__isa -> Shape)
c.describe          // A red shape (method found the same way)
print c.radius      // 10 (found via c.__isa -> Circle)
```

Here, `c` doesn't have `color` or `describe` directly, but MiniScript walks the chain: `c` -> `Circle` -> `Shape`, and finds them there.

**Overriding and still accessing the parent:**

If a subclass overrides a method but you want to also invoke the parent version, use `super`:

```
Shape = {}
Shape.describe = function
    print "A shape with " + self.sides + " sides"
end function

Triangle = new Shape
Triangle.sides = 3
Triangle.describe = function
    super.describe
    print "  (it's a triangle!)"
end function

t = new Triangle
t.describe
// A shape with 3 sides
//   (it's a triangle!)
```

**Key points:**
- Property reads automatically check `__isa` parents. You just use `self.propName` and it works.
- `super` is only needed when you've overridden a method in the current prototype and want to call the parent's version of that same method.
- The lookup chain can be as many levels deep as you like.

## `super`

**User:** What does `super` do?

**Assistant:** `super` is a keyword you use inside a method to invoke the parent prototype's version of that same method. It works just like `self`, except the property lookup starts one level up the `__isa` chain — it skips the current object's prototype and begins searching from the grandparent.

This is most useful when you override a method but still want to include the behavior defined in the parent.

**Basic example — overriding and calling the parent method:**

```
Animal = {}
Animal.describe = function
    print self.name + " is an animal"
end function

Dog = new Animal
Dog.describe = function
    super.describe    // calls Animal.describe
    print "  ...specifically, a dog!"
end function

rex = new Dog
rex.name = "Rex"
rex.describe
// Output:
// Rex is an animal
//   ...specifically, a dog!
```

Notice that even though `super.describe` calls the `Animal` version, `self` inside that parent method still refers to `rex` (the actual instance). So `self.name` correctly prints "Rex".

**Multi-level example:**

```
Shape = {}
Shape.describe = function
    print "I am a shape"
end function

Polygon = new Shape
Polygon.describe = function
    super.describe
    print "  with " + self.sides + " sides"
end function

RegularPolygon = new Polygon
RegularPolygon.describe = function
    super.describe
    print "  and all sides equal"
end function

hex = new RegularPolygon
hex.sides = 6
hex.describe
// Output:
// I am a shape
//   with 6 sides
//   and all sides equal
```

Each level calls `super.describe`, which chains up through `RegularPolygon` -> `Polygon` -> `Shape`, so all three messages print in order.

**Key points to remember:**

- `super` is only meaningful inside a method invoked via dot syntax.
- `super.foo` starts the lookup from the parent of the prototype where the current method is defined, not from `self.__isa`. This means it always goes exactly one level up from the method's own prototype, even if the instance is further down the chain.
- You can use `super` to access properties too, not just methods. For example, `super.sound` would retrieve the `sound` property from the parent prototype.

## File operations

**User:** How do I read and write files in MiniScript?

**Assistant:** In command-line MiniScript and Mini Micro, you can use the `file` module to read and write text files.

**Reading a file:**

```
content = file.readLines("/path/to/myfile.txt")
// Returns a list of strings, one per line

for line in content
    print line
end for
```

Or read the entire file as a single string:

```
text = file.open("/path/to/myfile.txt").read
```

**Writing a file:**

```
// Write a list of lines
lines = ["line 1", "line 2", "line 3"]
file.writeLines "/path/to/output.txt", lines
```

Or write a single string:

```
file.open("/path/to/output.txt", "w").write "Hello, file!"
```

**Appending to a file:**

```
f = file.open("/path/to/log.txt", "a")
f.write "New log entry" + char(10)
f.close
```

In **Mini Micro**, file paths are relative to the virtual filesystem. Common paths include:
- `/usr/` — user files
- `/sys/` — system files (read-only)

```
file.writeLines "/usr/mydata.txt", ["apple", "banana", "cherry"]
data = file.readLines("/usr/mydata.txt")
print data   // ["apple", "banana", "cherry"]
```

Note: File I/O availability depends on the MiniScript host environment. The command-line tool and Mini Micro both support it, but a web-based MiniScript environment may not.

## Listing files and directories

**User:** How do I list the files in a directory in MiniScript?

**Assistant:** Use `file.children` to get a list of files and directories within a given path:

```
items = file.children("/usr/")
for item in items
    print item
end for
```

Each entry is a string with the full path. You can check whether an entry is a file or directory using `file.info`:

```
items = file.children("/usr/")
for item in items
    info = file.info(item)
    if info.isDirectory then
        print "[DIR]  " + item
    else
        print "[FILE] " + item + " (" + info.size + " bytes)"
    end if
end for
```

The `file.info` function returns a map with properties like `size`, `date`, and `isDirectory`.

In **Mini Micro**, common directories include `/usr/` (user files) and `/sys/` (system files). In command-line MiniScript, you can use standard filesystem paths for your operating system.

## Recursion

**User:** Can I write a recursive function MiniScript?

**Assistant:** Yes! MiniScript fully supports recursive functions. A recursive function is one that calls itself, and it works just like in other languages. The key requirement is that you need a base case to stop the recursion, or you'll get a stack overflow error.

Here's a simple example that computes a factorial:

```
factorial = function(n)
    if n <= 1 then return 1
    return n * factorial(n - 1)
end function

print factorial(5)   // prints 120
```

`factorial(5)` calls `factorial(4)`, which calls `factorial(3)`, and so on, until `n` reaches 1. That's the base case, which returns 1 and stops the recursion. The results then multiply back up the chain: 1 * 2 * 3 * 4 * 5 = 120.

A couple of things to keep in mind:

- Always include a base case that returns without calling itself again
- Recursion isn't ideal for problems that recurse thousands of levels deep, or recurse multiple times per call; for those cases, consider rewriting with a `while` loop instead

## What is Mini Micro?

**User:** What is Mini Micro?

**Assistant:** Mini Micro is a virtual computer (sometimes called a "fantasy console" or "fantasy computer") that uses MiniScript as its built-in programming language. It provides a complete, self-contained environment for writing and running MiniScript programs.

Key features of Mini Micro include:

- A built-in code editor, so you can write and run code without any external tools
- A 960x640 pixel display with 8 layers that can each independently be one of five types: text display, pixel (bitmap) display, sprite layer, tile map, or solid color — this layered system makes it easy to build games and visual applications
- Keyboard, mouse, and gamepad input support
- Sound capabilities for playing and synthesizing sounds
- A virtual filesystem for saving and loading files, including code and data

Mini Micro is designed to be an approachable environment for learning programming and making games. Because MiniScript emphasizes readability and simplicity, and Mini Micro provides everything you need in one package, beginners can start creating interactive programs right away without dealing with complex development tool setup.

You can download Mini Micro for free from https://miniscript.org/MiniMicro/. It runs on Mac, Windows, and Linux. There is also a web-based version you can try directly in your browser.

## Mini Micro basics

**User:** What are the basic commands for working in Mini Micro?

**Assistant:** Mini Micro has a built-in command-line environment where you can type commands directly. Here are the essentials:

**`edit`** — Opens the built-in code editor where you write your program. Press Control-W or click the Close button to return to the command line.  Optionally, you may give `edit` a file name to load and then edit.

**`run`** — Runs the program currently in the editor.  Like `edit`, you make give `run` a file name to load and run.

**`save "filename"`** — Saves the current program to a file:
```
save "/usr/myProgram.ms"
```

You may omit the filename when saving a previously loaded or saved program.  When you supply a file name, it may be a full path as shown here, or just the name of a program in the current directory.  The ".ms" extension is optional in both cases.

**`load "filename"`** — Loads a program from a file into memory, making it the current program:
```
load "/usr/myProgram.ms"
```

Again you may supply a full or partial path, with or without ".ms".

**`dir`** — Lists files in the current directory.

**`cd "path"`** — Changes the current directory.  `cd` by itself takes you back to "/usr".

You can also type and run MiniScript code directly at the command prompt without using the editor:

```
> print "Hello!"
Hello!
> x = 2 + 3
> x
5
```

Common workflow:
1. Type `edit` to open the editor
2. Write your program
3. Press Control-W to exit the editor
4. Type `run` to execute it
5. Type `save "myProgram"` to save
6. Later, `load "myProgram"` to load it back

The `/usr/` directory is the main place to save your files. The `/sys/` directory contains system files and libraries, and is read-only.

## Keyboard input in Mini Micro

**User:** How do I check for keyboard input in a Mini Micro program?

**Assistant:** Mini Micro provides the `key` module for keyboard input.

**Check if any key is available:**

```
while true
    if key.available then
        k = key.get
        print "You pressed: " + k
    end if
    yield
end while
```

`key.available` returns `true` if a keypress is waiting; `key.get` retrieves it as a string.

**Check if a specific key is currently held down:**

```
while true
    if key.pressed("space") then print "Space is held!"
    if key.pressed("left") then print "Left arrow!"
    if key.pressed("right") then print "Right arrow!"
    yield
end while
```

`key.pressed` checks the real-time state of a key, which is better for game controls.

**Common key names** for `key.pressed`: `"left"`, `"right"`, `"up"`, `"down"`, `"space"`, `"return"`, `"escape"`, `"tab"`, or any letter like `"a"`, `"w"`, etc.

**Simple input example — move a character:**

```
x = 480
y = 320
while true
    if key.pressed("left") then x -= 3
    if key.pressed("right") then x += 3
    if key.pressed("up") then y += 3
    if key.pressed("down") then y -= 3

    gfx.clear
    gfx.fillEllipse x-10, y-10, 20, 20, color.green
    yield
end while
```

Note the `yield` call in the loop — this is essential in Mini Micro to give the system time to process events and update the display.

## Colors in Mini Micro

**User:** How do I work with colors in Mini Micro?

**Assistant:** Mini Micro represents colors as strings in `"#RRGGBB"` or `"#RRGGBBAA"` hex format. The `color` module provides many predefined colors.

**Predefined colors:**

```
print color.red      // #FF0000
print color.green    // #00FF00
print color.blue     // #0000FF
print color.white    // #FFFFFF
print color.black    // #000000
print color.yellow   // #FFFF00
print color.orange   // #FF8800
```

**Creating custom colors:**

Use the `color.rgb` or `color.rgba` functions:

```
myColor = color.rgb(128, 0, 255)       // purple
print myColor                           // #8000FF

semiTransparent = color.rgba(255, 0, 0, 128)  // semi-transparent red
print semiTransparent                           // #FF000080
```

Arguments are 0–255 for each channel (red, green, blue, and optionally alpha).

**Using colors for drawing:**

```
gfx.fillRect 100, 100, 200, 150, color.blue
gfx.drawRect 100, 100, 200, 150, color.white

gfx.fillEllipse 400, 300, 80, 80, color.rgb(255, 128, 0)
```

**Using colors with text:**

```
text.color = color.yellow
text.backColor = color.navy
print "Yellow on navy!"
```

You can also compare colors directly since they're just strings:

```
c = color.red
if c == "#FF0000" then print "It's red!"
```

## Text display formatting

**User:** How do I control text positioning and color on Mini Micro's text display?

**Assistant:** Mini Micro has a `text` display layer that works like a terminal grid with rows and columns.

**Setting cursor position:**

```
text.row = 15
text.column = 20
print "Hello!"   // prints at row 15, column 20
```

Rows are numbered from 0 (bottom) to 25 (top). Columns are numbered from 0 (left) to 67 (right).

**Setting text color and background:**

```
text.color = color.yellow
text.backColor = color.blue
print "Yellow text on blue background"
```

**Placing text at specific locations:**

```
text.row = 20
text.column = 30
text.color = color.lime
print "Score: 100"
```

**Clearing the text display:**

```
text.clear
```

**Writing a single character at a position:**

```
text.setCell 10, 5, "X"   // column 10, row 5, character "X"
```

**Getting info about a cell:**

```
ch = text.cell(10, 5)     // get character at column 10, row 5
```

**Practical example — a simple status bar:**

```
text.clear
text.row = 25
text.column = 0
text.color = color.white
text.backColor = color.gray
print " " * 68   // fill top row with gray
text.row = 25
text.column = 2
print "My Game v1.0"
text.backColor = color.black
```

## Pixel graphics with `gfx`

**User:** How do I draw shapes and lines on the screen in Mini Micro?

**Assistant:** Mini Micro has a `gfx` (pixel graphics) display layer for drawing shapes, lines, and pixels.

**Drawing rectangles:**

```
gfx.fillRect 100, 100, 200, 150, color.blue       // filled rectangle
gfx.drawRect 100, 100, 200, 150, color.white       // outline only
// Arguments: x, y, width, height, color
```

**Drawing ellipses (and circles):**

```
gfx.fillEllipse 400, 300, 100, 100, color.red      // filled circle
gfx.drawEllipse 400, 300, 100, 100, color.yellow    // circle outline
// For a circle, use the same width and height
```

**Drawing lines:**

```
gfx.line 0, 0, 960, 640, color.green
// Arguments: x1, y1, x2, y2, color
```

**Drawing individual pixels:**

```
gfx.setPixel 480, 320, color.white
```

**Clearing the screen:**

```
gfx.clear color.black   // clear to black
gfx.clear               // clear to transparent
```

**Example — drawing a simple scene:**

```
gfx.clear color.aqua
// Ground
gfx.fillRect 0, 0, 960, 200, color.green
// Sun
gfx.fillEllipse 750, 500, 80, 80, color.yellow
// House
gfx.fillRect 300, 200, 200, 150, color.brown
gfx.fillPoly [[300, 350], [400, 450], [500, 350]], color.red
// Door
gfx.fillRect 370, 200, 60, 100, color.maroon
```

The screen is 960x640 pixels by default, with (0,0) at the bottom-left corner.

## Loading and drawing images

**User:** How do I load and draw an image in Mini Micro?

**Assistant:** Use `file.loadImage` to load an image file, then draw it on the `gfx` display layer.

**Loading and drawing an image:**

```
img = file.loadImage("/sys/pics/Wumpus.png")
gfx.drawImage img, 300, 100  // draw with lower-left corner at x=300, y=100
```

**Drawing at a specific size:**

```
gfx.drawImage img, 100, 100, 200, 150
// Arguments: image, left, bottom, width, height (scales the image)
```

**Getting image info:**

```
print img.width    // width in pixels
print img.height   // height in pixels
```

**Drawing part of an image (source rect):**

```
gfx.drawImage img, 100, 100, 64, 64, 0, 0, 32, 32
// Draws a 32x32 portion (from bottom-left of image) scaled to 64x64 on screen
```

**Using images with sprites (more common for games):**

```
img = file.loadImage("/sys/pics/animals/cat.png")
sp = new Sprite
sp.image = img
sp.x = 480
sp.y = 320
display(4).sprites.push sp
```

Mini Micro supports PNG files with or without transparency, as well as JPEG files.
```

## Display layers in Mini Micro

**User:** How do Mini Micro's display layers work?

**Assistant:** Mini Micro has 8 display layers, numbered 0 through 7, stacked from front (0) to back (7). Each layer can be independently configured as one of several display types.

**The default layer setup:**

- `display(0)` — off
- `display(1)` — off
- `display(2)` — off
- `display(3)` — TextDisplay (`text` - where `print` and `input` go)
- `display(4)` — SpriteDisplay (where sprites live)
- `display(5)` — PixelDisplay (`gfx` — the default drawing target)
- `display(6)` — off
- `display(7)` — SolidColor (background)

**Accessing a specific layer:**

```
layer = display(5)
layer.clear color.black
```

**Changing a layer's mode:**

You can change the display mode of any layer by assigning to its `.mode` property:
```
display(4).mode = displayMode.pixel
```

Note that this actually changes the object that `display(n)` returns.  So, if you're going to get and keep a reference to a display for future use, you should always do this _after_ setting the mode:

```
display(4).mode = displayMode.pixel
gfx2 = display(4)
```

**Pointing `gfx` or `text` to a specific layer:**

`gfx` and `text` are global variables automatically set on boot (or by the `clear` command) to point to display 5 and 3, respectively.  But you can reassign them as you wish:

```
display(6).mode = displayMode.text
text = display(6)    // now text commands output on layer 6
display(3).mode = displayMode.pixel
gfx = display(3)    // now gfx commands draw on layer 3
```

## Mouse input in Mini Micro

**User:** How do I get mouse input in Mini Micro?

**Assistant:** Mini Micro provides the `mouse` module for tracking the mouse position and button state.

**Getting mouse position:**

```
while true
    text.clear
    print "Mouse X: " + mouse.x
    print "Mouse Y: " + mouse.y
    yield
end while
```

`mouse.x` and `mouse.y` give the current position in screen coordinates (0–959 x, 0–639 y, with origin at bottom-left).

**Checking mouse button state:**

```
while true
    if mouse.button then
        gfx.fillEllipse mouse.x-5, mouse.y-5, 10, 10, color.red
    end if
    yield
end while
```

`mouse.button` returns `1` (true) when the left mouse button is held down, and `0` (false) otherwise.  To check other buttons, supply a button number; for example, `mouse.button(1)` reports whether the right mouse button is currently pressed.

**Detecting clicks (press and release):**

```
wasDown = false
while true
    if mouse.button and not wasDown then
        // Mouse was just clicked
        print "Click at " + mouse.x + ", " + mouse.y
    end if
    wasDown = mouse.button
    yield
end while
```

**Practical example — a simple drawing program:**

```
gfx.clear color.white
while true
    if mouse.button then
        gfx.fillEllipse mouse.x-3, mouse.y-3, 6, 6, color.black
    end if
    yield
end while
```

Remember to include `yield` in your loop to give the system time to update.  Press Control-C to break out of the infinite loop.

## The `import` command

**User:** How do I use the `import` command in Mini Micro?

**Assistant:** The `import` command loads and runs another MiniScript file, making its global variables and functions available in your program.

**Basic usage:**

```
import "mathUtil"
```

This looks for a file named `stringUtil.ms` in the standard library paths. After importing, any globals defined in that file are available in a map named `mathUtil`

```
print mathUtil.dice(6, 2)  // returns the sum of two six-sided die rolls
```

**Where Mini Micro looks for imports:**

The search path for imports is determined by `env.importPaths`, which by default is:

1. The current directory
2. `/usr/lib/`
3. `/sys/lib/`

Mini Micro comes with several useful libraries in `/sys/lib/`, including:
- `stringUtil` — extra string functions
- `listUtil` — extra list functions like `list.init2d`
- `mathUtil` — extra math functions
- `mapUtil` — extra map functions
- `qa` — quality assurance functions (`assert`, etc.)
- `json` — JSON parsing and generation

**Importing your own files:**

If you have a file at `/usr/lib/myHelpers.ms`, you can import it:

```
import "myHelpers"
```

**Important notes:**
- You don't include the `.ms` extension in the import string
- `import` runs the file, so any top-level code in the imported file will execute
- If the same file is imported more than once, it runs every time
- `import` is a feature of the Mini Micro environment (and some others), not a feature of the MiniScript language itself

## Playing sounds in Mini Micro

**User:** How do I play sounds in Mini Micro?

**Assistant:** Mini Micro can play sound files using the `Sound` class.

**Loading and playing a sound:**

```
snd = file.loadSound("/sys/sounds/hit.wav")
snd.play
```

**Controlling volume and speed:**

```
snd = file.loadSound("/sys/sounds/twinkle.wav")
snd.play 0.5    // play at half volume (0 to 1 range)
snd.play 1, 2   // full volume, double speed (higher pitch)
```

**Checking if a sound is playing:**

```
snd.play
while snd.isPlaying
    yield
end while
print "Sound finished!"
```

**Stopping a sound:**

```
snd.stop
```

**Playing background music:**

```
music = file.loadSound("/usr/myMusic.ogg")
music.loop     // plays the sound on repeat
// Later:
music.stop     // stop the music
```

Mini Micro includes some built-in sounds in `/sys/sounds/`. You can also load your own `.wav` or `.ogg` files from `/usr/`.

**Quick beep (without loading a file):**

Mini Micro has a built-in "terminal bell" that plays whenever you print `char(7)`, for example:
```
print "ERROR!" + char(7)
```

**Synthesized sounds**

Mini Micro has a sophisticated system for synthesizing sounds on the fly.  You can import "/sys/lib/sounds" for a built-in selection of synthesized sounds, and examine that code to see how they are made.  The demo at "/sys/demo/soundLab" is another good way to develop synthesized sounds.

## Sound synthesis

**User:** How do I create sounds from scratch (synthesis) in Mini Micro?

**Assistant:** Mini Micro can generate sounds programmatically using `Sound.init`, which takes four parameters:

1. Duration: how long the sound should be, in seconds
2. Frequency: how many times the waveform should repeat per second
3. Envelope: how the volume of the sound should change over its duration
4. Waveform: what one cycle of the sound looks like

Frequency and envelope can be a single value, or a list of values; in the latter case, the frequency or amplitude is interpolated over the given values.  Waveform is typically one of the built-in `Sound.sineWave`, `Sound.squareWave`, etc., but can also be individual samples as a list.  Moreover, sounds can be mixed (with the `.mix` method, allowing you to build up complex layered sounds.

Here's an example:

```
bounce = new Sound
bounce.init 0.3, [100,1000], [1,0], Sound.sawtoothWave
bounce.play
```

This makes a sound 0.3 seconds long, with a frequency that starts at 100 Hz and rises to 1000 Hz by the end of the sound.  The amplitude starts at 1 (full volume) and fades to 0 by the end, and it uses a sawtooth wave, which gives a retro, 8-bit feel to the sound.

A good way to learn to make your own synthesized sounds is to load "/sys/lib/sounds", run it to hear what the provided sounds sound like, and then `edit` to see the code that creates them.  Another good tool is "/sys/demo/soundLab", which provides a graphical interface for building your own synthesized sounds, and then provides the corresponding MiniScript code.

## Subclasses and `super`

**User:** How do I create a subclass that extends a parent class in MiniScript, and how do I call the parent's method?

**Assistant:** In MiniScript's prototype-based OOP, you create a "subclass" by using `new` on the parent prototype, then overriding or adding methods.

**Creating a subclass:**

```
Animal = {}
Animal.name = "unknown"
Animal.speak = function
    print self.name + " makes a sound"
end function

Dog = new Animal
Dog.speak = function
    print self.name + " says Woof!"
end function

Cat = new Animal
Cat.speak = function
    print self.name + " says Meow!"
end function
```

**Calling the parent's method with `super`:**

Use `super` inside a method to call the parent (prototype) version of that method:

```
Animal = {}
Animal.describe = function
    print self.name + " is an animal"
end function

Dog = new Animal
Dog.describe = function
    super.describe    // calls Animal.describe
    print "  ...specifically, a dog!"
end function

rex = new Dog
rex.name = "Rex"
rex.describe
// Rex is an animal
//   ...specifically, a dog!
```

`super` works like `self`, but starts the method lookup one level up the `__isa` chain, skipping the current prototype.

**Multi-level inheritance:**

```
Animal = {}
Animal.legs = 4

Pet = new Animal
Pet.owner = "unknown"

Dog = new Pet
Dog.sound = "Woof"

myDog = new Dog
myDog.name = "Rex"
myDog.owner = "Alice"
print myDog.legs    // 4 (inherited from Animal)
print myDog.owner   // Alice (set on instance, overrides Pet default)
```

The `__isa` chain is: `myDog` → `Dog` → `Pet` → `Animal`.

## The `yield` function

**User:** What does `yield` do in MiniScript, and when should I use it?

**Assistant:** `yield` pauses execution momentarily to let the host environment process events and update the display.  In Mini Micro, it also waits until the start of the next display frame (which happens 60 times per second).  It's essential in Mini Micro for game loops and animations.

**Why you need it:**

Without `yield`, a tight loop will run as fast as your machine can make it go, which will vary from machine to machine, making the result unpredictable.  Also, the display updates at no more than 60 frames per second, so your processing would be out of sync with the display.  With `yield` in your main loop, your game runs at the same rate as the display updates, and at the same speed on all machines.

**Basic game loop pattern:**

```
while true
    yield
    // update game state
end while
```

**Example — animation:**

```
x = 0
while x < 960
    yield
    gfx.clear
    gfx.fillEllipse x, 320, 30, 30, color.red
    x += 3
end while
```

**`yield` is also like `wait`:**

The `wait` function pauses for a specific amount of time (in seconds). `yield` is essentially `wait(0.01)` — a very brief pause (about 1/60th of a second by default, synced to the frame rate).

```
wait 2.0    // pause for 2 seconds
yield       // pause for the rest of the frame (~1/60s)
```

**In command-line MiniScript:**

`yield` has minimal effect in command-line MiniScript (no display to update), but it's still good practice in long-running loops to keep the system responsive.

**Key rule:** If your program has a loop that runs continuously (game loop, animation, input polling), always include `yield` in the loop body.

## Sprites in Mini Micro

**User:** How do I create and use sprites in Mini Micro?

**Assistant:** Sprites are images that can be moved around the screen independently. They live on a SpriteDisplay layer.

**Creating a sprite:**

```
sp = new Sprite
sp.image = file.loadImage("/sys/pics/animals/cat.png")
sp.x = 480
sp.y = 320
display(4).sprites.push sp
```

This loads an image, positions the sprite at the center of the screen, and adds it to the default sprite display layer (layer 4).

**Moving a sprite:**

```
sp.x = 200
sp.y = 400
```

Just change `.x` and `.y` and the sprite moves automatically on the next frame.

**Scaling and rotating:**

```
sp.scale = 2        // double size
sp.scale = 0.5      // half size
sp.rotation = 45    // rotate 45 degrees
```

**Tinting:**

```
sp.tint = color.red   // tint the sprite red
```

**Simple example — move a sprite around the screen:**

```
clear
sp = new Sprite
sp.image = file.loadImage("/sys/pics/animals/dog.png")
sp.x = 480
sp.y = 320
display(4).sprites.push sp

while true
    sp.x += key.axis("Horizontal") * 3
    sp.y += key.axis("Vertical") * 3
    yield
end while
```

(Note that `key.axis` allows you to use WASD, arrow keys, or a gamepad.)

**Removing a sprite:**

```
idx = display(4).sprites.indexOf(sp)
if idx != null then display(4).sprites.remove idx
```

Sprites are drawn in order — later sprites in the list appear in front of earlier ones.

## Sprite animation

**User:** How do I animate a sprite in Mini Micro?

**Assistant:** There are two main ways to animate sprites in Mini Micro: frame-based animation (swapping images) and movement animation.

**Frame-based animation (sprite sheet):**

Load multiple frames and cycle through them:

```
frames = []
frames.push file.loadImage("/sys/pics/KP/KP-run1.png")
frames.push file.loadImage("/sys/pics/KP/KP-run2.png")

sp = new Sprite
sp.image = frames[0]
sp.x = 480
sp.y = 320
display(4).sprites.push sp

frame = 0
timer = 0
while true
    timer += 1
    if timer % 8 == 0 then   // change frame every 8 ticks
        frame = (frame + 1) % frames.len
        sp.image = frames[frame]
    end if
    yield
end while
```

**Movement animation:**

```
clear
sp = new Sprite
sp.image = file.loadImage("/sys/pics/animals/cat.png")
sp.x = 100
sp.y = 320
display(4).sprites.push sp

// Smooth movement
while sp.x < 800
    sp.x += 2
    sp.y = 320 + sin(sp.x * 0.05) * 50  // bouncy path
    yield
end while
```

**Rotation animation:**

```
sp = new Sprite
sp.image = file.loadImage("/sys/pics/shapes/Star.png")
sp.x = 480
sp.y = 320
display(4).sprites.push sp

while true
    yield
    sp.rotation += 2   // rotate 2 degrees per frame
end while
```

**Combining movement and frames:**

```
while true
    if key.pressed("right") then
        sp.x += 3
        timer += 1
        if timer % 8 == 0 then
            frame = (frame + 1) % frames.len
            sp.image = frames[frame]
        end if
    end if
    yield
end while
```

The key idea is to update sprite properties (`.image`, `.x`, `.y`, `.rotation`, `.scale`) each frame inside a `while` loop with `yield`.

## Collision detection with `Bounds`

**User:** How do I detect collisions between sprites in Mini Micro?

**Assistant:** Mini Micro provides a `Bounds` class for axis-aligned bounding box (AABB) collision detection between sprites.  To use this, set up `localBounds` on each sprite with a `Bounds` reflecting the sprite's collision box.

**Basic collision check using `overlaps`:**

```
clear
sp1 = new Sprite
sp1.image = file.loadImage("/sys/pics/animals/cat.png")
sp1.x = 200; sp1.y = 300
sp1.localBounds = new Bounds
sp1.localBounds.width = sp1.image.width
sp1.localBounds.height = sp1.image.height
display(4).sprites.push sp1

sp2 = new Sprite
sp2.image = file.loadImage("/sys/pics/animals/dog.png")
sp2.x = 400; sp2.y = 300
sp2.localBounds = new Bounds
sp2.localBounds.width = sp2.image.width
sp2.localBounds.height = sp2.image.height
display(4).sprites.push sp2

while true
	sp1.x += key.axis("Horizontal") * 5
	sp1.y += key.axis("Vertical") * 5
	
	if sp1.overlaps(sp2) then
		text.row = 25
		text.column = 0
		print "Collision!"
	else
		text.clear
	end if
	yield
end while
```

The `overlaps` method on a sprite checks if its bounding box intersects another sprite's bounding box.

**Point containment:**

Check if a point (like the mouse) is inside a sprite's bounds:

```
if sp1.contains(mouse.x, mouse.y) then
    print "Mouse is over the sprite!"
end if
```

This requires you to have set up `localBounds`, as above.

**Tips:**
- You must always set `.localBounds` for `.overlaps` and `.contains` to work
- You can also do your own collision checking, for example, by computing the distance between two round sprites
- For pixel-perfect collision, you would need to check individual pixels, which is more complex

## Weighted random selection

**User:** How can I pick a random item from a list where some items are more likely than others?

**Assistant:** You can use weighted random selection by assigning weights to each item and picking based on a random number within the total weight.

```
weightedPick = function(items, weights)
    total = weights.sum
    r = rnd * total
    cumulative = 0
    for i in items.indexes
        cumulative += weights[i]
        if r < cumulative then return items[i]
    end for
    return items[-1]
end function
```

Usage:

```
items = ["common", "uncommon", "rare", "legendary"]
weights = [60, 25, 12, 3]

for i in range(1, 10)
    print weightedPick(items, weights)
end for
```

In this example, "common" has a 60% chance, "uncommon" 25%, "rare" 12%, and "legendary" 3%.

**Alternative approach using a map:**

```
lootTable = {"gold coin": 50, "silver ring": 30, "magic sword": 15, "dragon egg": 5}

weightedPick = function(table)
    total = 0
    for kv in table
        total += kv.value
    end for
    r = rnd * total
    cumulative = 0
    for kv in table
        cumulative += kv.value
        if r < cumulative then return kv.key
    end for
end function

print weightedPick(lootTable)
```

The core idea: generate a random number from 0 to the total weight, then walk through the items adding up weights until you pass the random number.

## The `isa` operator

**User:** How do I check whether an object is an instance of a particular type or class in MiniScript?

**Assistant:** Use the `isa` operator. It checks whether a value is of a given type or inherits from a given prototype.

**Checking built-in types:**

```
x = 42
print x isa number    // 1 (true)
print x isa string    // 0 (false)

s = "hello"
print s isa string    // 1 (true)

lst = [1, 2, 3]
print lst isa list    // 1 (true)

m = {"a": 1}
print m isa map       // 1 (true)
```

**Checking custom prototypes:**

```
Animal = {}
Dog = new Animal
Cat = new Animal

rex = new Dog

print rex isa Dog      // 1 (true)
print rex isa Animal   // 1 (true — Dog inherits from Animal)
print rex isa Cat      // 0 (false)
print rex isa map      // 1 (true — all objects are maps)
```

`isa` walks the entire `__isa` chain, so it works for multi-level inheritance.

**Checking for null and funcRef:**

```
x = null
print x isa null       // equivalent to: print x == null

f = @print
print f isa funcRef    // 1 (true)
```

**Practical use — type-safe function:**

```
process = function(val)
    if val isa number then
        print "Number: " + val * 2
    else if val isa string then
        print "String: " + val.upper
    else if val isa list then
        print "List with " + val.len + " items"
    end if
end function
```

## TileDisplay basics

**User:** How do I set up and use a TileDisplay in Mini Micro?

**Assistant:** A TileDisplay shows a grid of small images (tiles) — perfect for maps, levels, and tile-based games.

**Setting up a TileDisplay:**

```
clear
display(4).mode = displayMode.tile
td = display(4)

// Load a tile set image
td.tileSet = file.loadImage("/sys/pics/TileShapes.png")
td.tileSetTileSize = 64   // each tile is 64x64 pixels in the tile set
td.cellSize = 64           // each cell on screen is 64x64 pixels

td.extent = [15, 10]       // grid is 15 columns by 10 rows
td.clear 16  // clear all cells to tile 16```

**Setting tiles in cells:**

```
td.setCell 0, 0, 1    // set column 0, row 0 to tile index 1
td.setCell 5, 3, 4    // set column 5, row 3 to tile index 4
td.setCell 3, 0, null // clear the tile in column 3, row 0
```

Setting a cell to null makes it empty/transparent. Indices count left-to-right, top-to-bottom across the tile set image.  The `view` command provides a quick way to look up tile indexes:

```
view td.tileSet
```

**Filling a grid:**

The `setCell` method accepts a list of coordinates for both X and Y, which can be combined to fill a rectangular range of cells all at once:
```
td.setCell range(4, 14), range(0, 9), 22
```

**Getting a tile value:**

```
tileIdx = td.cell(5, 3)
print tileIdx
```

**Scrolling the tile display:**

```
td.scrollX = 100   // scroll 100 pixels right
td.scrollY = 50    // scroll 50 pixels up
```

This is useful for side-scrolling or top-down games where the map is larger than the screen.

**Practical tip:** Design your tile set image as a grid of equally-sized tiles. The `tileSetTileSize` tells Mini Micro how to slice up that image into individual tiles.

## Tile sets and cell indexing

**User:** How do tile sets work in Mini Micro? How do I specify which tile appears in each cell?

**Assistant:** A tile set is a single image containing all your tiles arranged in a grid. Mini Micro slices it up based on the tile size you specify.

**How tile indexing works:**

Tiles are numbered starting from 0, reading left-to-right, top-to-bottom across the tile set image:

```
// If your tile set is 4 tiles wide:
// Index:  0  1  2  3
//         4  5  6  7
//         8  9  10 11
```

**Setting up the tile set:**

```
display(4).mode = displayMode.tile
td = display(4)
td.tileSet = file.loadImage("/sys/pics/SimplePlatformTiles.png")
td.tileSetTileSize = 32   // each tile is 32x32 in the image
td.cellSize = 32           // each cell on screen is 32x32
```

**Placing tiles:**

```
td.setCell 0, 0, 1    // place tile #1 at column 0, row 0
td.setCell 1, 0, 3    // place tile #3 at column 1, row 0
td.setCell 2, 0, null // tile 0 = empty/blank
```

**Building a map from data:**

```
mapData = [[1, 1, 1, 1, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 0, 0, 1],
           [1, 0, 2, 0, 1],
           [1, 1, 1, 1, 1]]

for row in mapData.indexes
    for col in mapData[row].indexes
        td.setCell col, mapData.len - 1 - row, mapData[row][col]
    end for
end for
```

Note: row 0 in TileDisplay is at the bottom of the screen, so you may need to flip your data if you define it top-to-bottom, as shown above.

**Tile tinting:**

You can tint individual cells:

```
td.setCellTint 5, 3, color.red   // tint the cell at (5,3) red
```

This lets you reuse the same tile with different colors.

## Hex grids with TileDisplay

**User:** Can Mini Micro's TileDisplay support hexagonal grids?

**Assistant:** Yes! Mini Micro's TileDisplay has built-in support for hexagonal grids. You enable it by setting the `oddRowOffset` or `oddColOffset` property.

**Setting up a hex grid (offset rows):**

```
display(4).mode = displayMode.tile
td = display(4)
td.tileSet = file.loadImage("/sys/pics/hextiles-55x64.png")
td.tileSetTileSize = [55, 64]
td.cellSize = [55, 64]
td.extent = [10, 8]
td.clear 0
td.oddRowOffset = 0.5    // offset odd rows by half a cell width
td.overlap = [0, 16]   // overlap vertically for tight packing
```

The key properties:
- `oddRowOffset` — shifts odd-numbered rows by this fraction of a cell width (0.5 for hex grids)
- `overlap` — controls spacing between cells; for hex tiles that are taller than wide, an overlap of 1/4 the cell height is typical

**Filling the hex grid:**

```
for col in range(td.extent[0] - 1)
    for row in range(td.extent[1] - 1)
        td.setCell col, row, floor(rnd * 6)
    end for
end for
```

The cell addressing still uses column and row numbers just like a regular grid — the display handles the visual offset automatically.

**Tips for hex grids:**
- Design your hex tile images to overlap slightly so they tessellate properly
- `oddColOffset` works similarly but shifts odd columns vertically instead
- The coordinate system is still rectangular — the visual offset is purely a display feature
- For hex grid neighbor calculations, remember that odd and even rows have different neighbor offsets

## Using `list.init2d` from listUtil

**User:** How do I create a 2D array in MiniScript?

**Assistant:** MiniScript doesn't have a built-in 2D array type, but you can use a list of lists. The `listUtil` library provides a convenient `list.init2d` function for this.

**Using `list.init2d` (recommended):**

```
import "listUtil"

grid = list.init2d(5, 3, 0)   // 5 rows, 3 columns, filled with 0
grid[2][1] = 42
print grid[2][1]   // 42
```

**Why you need `list.init2d`:**

You might be tempted to do this:

```
// WRONG — all rows share the same inner list!
grid = [[0]*5] * 3
grid[0][0] = 99
print grid[1][0]   // 99 — oops, all rows changed!
```

The `*` operator on lists creates references to the same list, not copies. `list.init2d` avoids this by creating independent lists for each row.

**Building it manually:**

If you don't want to import `listUtil`:

```
rows = 3
cols = 5
grid = []
for r in range(1, rows)
    grid.push [0] * cols
end for
```

**Iterating a 2D array:**

```
for row in grid.indexes
    for col in grid[row].indexes
        // do something with grid[row][col]
    end for
end for
```

## Factory methods on classes

**User:** What's a good pattern for creating objects with specific initial values in MiniScript?

**Assistant:** Since MiniScript has no constructors, the idiomatic approach is to define a **factory method** (often called `Make` or `Create`) on the prototype.  This method can use `new self` to create the new instance of the correct type even when it has been subclassed.

**Factory method pattern:**

```
Vector = {}
Vector.x = 0
Vector.y = 0

Vector.Make = function(x, y)
    v = new self
    v.x = x
    v.y = y
    return v
end function

Vector.magnitude = function
    return sqrt(self.x^2 + self.y^2)
end function

v = Vector.Make(3, 4)
print v.x              // 3
print v.magnitude      // 5
```

**With default values:**

```
Enemy = {}
Enemy.name = "unknown"
Enemy.hp = 100
Enemy.speed = 1

Enemy.Make = function(name, hp=100, speed=1)
    e = new self
    e.name = name
    e.hp = hp
    e.speed = speed
    return e
end function

goblin = Enemy.Make("Goblin", 30, 2)
dragon = Enemy.Make("Dragon", 500)
```

**Why not just set properties after `new`?**

You can, but a factory method is cleaner when you have multiple properties to initialize, and it keeps the creation logic in one place:

```
// Without factory method — works but verbose:
goblin = new Enemy
goblin.name = "Goblin"
goblin.hp = 30
goblin.speed = 2

// With factory method — clean and concise:
goblin = Enemy.Make("Goblin", 30, 2)
```

**Naming convention:** `Make` is the most common name for factory methods in MiniScript, but `Create`, `Init`, or any clear name works.  (By convention, methods intended to be invoked on the prototype, rather than on an instance, are capitalized.)

## Debugging infinite loops

**User:** My MiniScript program is stuck in an infinite loop. How do I figure out what's wrong?

**Assistant:** Here's a systematic approach to finding and fixing infinite loops:

**1. Stop the program:** In Mini Micro, press Ctrl+C to break out of a running program.

**2. Add debug prints:** Insert `print` statements inside the loop to see what's happening:

```
while someCondition
    print "loop: x=" + x + " y=" + y   // ADD THIS
    // ... rest of loop
end while
```

This shows you the values each iteration so you can spot why the exit condition is never met.

**3. Common causes:**

**Forgetting to update the loop variable:**
```
// BUG: i never changes!
i = 0
while i < 10
    print i
    // forgot: i += 1
end while
```

**Updating the wrong variable (scope issue):**
```
count = 0
decrement = function
    count = count - 1   // creates a LOCAL count, doesn't change outer!
end function

while count < 10
    decrement    // doesn't actually decrement outer count
end while
```
Fix: use `outer.count` in the function.

**Condition can never become false:**
```
x = 10
while x != 0
    x -= 3   // x goes 10, 7, 4, 1, -2, -5... never exactly 0!
end while
```
Fix: use `while x > 0` instead of `while x != 0`.

**Off-by-one with `range`:**
If you're not in an infinite loop but getting unexpected behavior, remember `range` is inclusive — `range(0, n)` produces n+1 values.

**4. Use `yield` in long loops:** Even if your loop is correct, adding `yield` ensures the display updates and runs at a steady speed:

```
while processing
    yield
    // heavy work here
end while
```

## Turtle graphics

**User:** How do I use t graphics in Mini Micro?

**Assistant:** Mini Micro includes a t graphics module. Import it to get started:

```
import "turtle"
t = new Turtle  // create a drawing t

// Move forward and turn, four times, making a square
t.penDown
t.forward 100
t.right 90
t.forward 100
t.right 90
t.forward 100
t.right 90
t.forward 100
```

**Key turtle commands:**

Assuming you have imported "turtle" and done `t = new Turtle`:

- `t.forward n` — move forward n pixels
- `t.backward n` — move backward n pixels
- `t.right degrees` — turn right
- `t.left degrees` — turn left
- `t.penDown = false` — stop drawing
- `t.penDown = true` — resume drawing
- `t.color = color.red` — set the pen color
- `t.penSize = 3` — set the pen width
- `t.goTo x, y` — move to a specific position (while drawing)
- `t.jumpTo x, y` — move to a specific position (without drawing)
- `t.heading = 90` — set the direction (0=right, 90=up)

**Drawing a circle:**

```
import "turtle"
t = new Turtle
for i in range(1, 360)
    t.forward 2
    t.right 1
end for
```

**Drawing a star:**

```
import "turtle"
t = new Turtle
t.color = color.yellow
for i in range(1, 5)
    t.forward 150
    t.right 144
end for
```

**Drawing a spiral:**

```
import "turtle"
t = new Turtle
t.color = color.lime
for i in range(1, 200)
    t.forward i
    t.right 91
end for
```

The turtlre starts at the center of the screen (480, 320), facing right. It draws on the `gfx` layer.

## Recursive drawing algorithms

**User:** How do I draw fractal-like shapes using recursion in Mini Micro?

**Assistant:** Combine turtle graphics with recursion to draw fractal patterns. Here are a couple of examples:

**Koch snowflake curve:**

```
import "turtle"
t = new Turtle

kochCurve = function(length, depth)
    if depth == 0 then
        t.forward length
    else
        kochCurve length/3, depth-1
        t.left 60
        kochCurve length/3, depth-1
        t.right 120
        kochCurve length/3, depth-1
        t.left 60
        kochCurve length/3, depth-1
    end if
end function

// Draw a Koch snowflake (3 sides)
t.jumpTo 200, 500
t.color = color.aqua

for i in range(1, 3)
    kochCurve 400, 3
    t.right 120
end for
```

**Recursive tree:**

```
import "turtle"
t = new Turtle

drawTree = function(branchLen, depth)
    if depth == 0 then return
    t.penSize = depth
    t.color = color.rgb(50, depth*30, 0)
    t.forward branchLen
    t.left 30
    drawTree branchLen * 0.7, depth - 1
    t.right 60
    drawTree branchLen * 0.7, depth - 1
    t.left 30
    t.backward branchLen
end function

t.jumpTo 480, 50
t.heading = 90
drawTree 120, 10
```

**Sierpinski triangle:**

```
import "turtle"
t = new Turtle

sierpinski = function(length, depth)
    if depth == 0 then
        for i in range(1, 3)
            t.forward length
            t.left 120
        end for
    else
        sierpinski length/2, depth-1
        t.forward length/2
        sierpinski length/2, depth-1
        t.backward length/2
        t.left 60
        t.forward length/2
        t.right 60
        sierpinski length/2, depth-1
        t.left 60
        t.backward length/2
        t.right 60
    end if
end function

t.jumpTo 180, 100
t.color = color.lime
sierpinski 500, 6
```

The key pattern: the recursive function draws a simpler version at smaller scale, calling itself for sub-parts.

## Cloning and mutating objects

**User:** How do I make a copy (clone) of a map and then modify it without affecting the original in MiniScript?

**Assistant:** Maps, like lists, are reference types in MiniScript. Assigning a map to a new variable doesn't copy it. To make an independent shallow copy, add an empty map to it with `+`:

```
original = {"name": "Alice", "age": 30}
clone = original + {}

clone.name = "Bob"
print original.name   // Alice (unaffected)
print clone.name      // Bob
```

**Why `original + {}`?** The `+` operator on maps merges the right map into the left, producing a new map. Adding `{}` gives you a fresh copy.

**Deep copy for nested maps:**

If your map contains lists or other maps, `original + {}` only makes a shallow copy — nested objects are still shared. For a deep copy:

```
deepCopyMap = function(m)
    result = {}
    for kv in m
        if kv.value isa map then
            result[kv.key] = deepCopyMap(kv.value)
        else if kv.value isa list then
            result[kv.key] = kv.value[:]
        else
            result[kv.key] = kv.value
        end if
    end for
    return result
end function

original = {"name": "Alice", "scores": [90, 85, 95]}
clone = deepCopyMap(original)
clone.scores.push 100
print original.scores   // [90, 85, 95] (unaffected)
print clone.scores      // [90, 85, 95, 100]
```

**Quick reference:**
- Shallow copy of a list: `copy = original[:]`
- Shallow copy of a map: `copy = original + {}`
- For simple maps (no nested collections), shallow copy is sufficient

## Where to get MiniScript help

**User:** Where can I go to get help with MiniScript programming or find example code?

**Assistant:** Here are the best resources for MiniScript help and examples:

**Official resources:**
- **MiniScript website:** https://miniscript.org — documentation, tutorials, and reference
- **MiniScript wiki:** https://miniscript.org/wiki — detailed language reference with examples
- **Quick Reference:** https://miniscript.org/files/MiniScript-QuickRef.pdf

**Community:**
- **MiniScript Discord:** Active community where you can ask questions and share projects
- **GitHub:** https://github.com/JoeStrout/miniscript — source code, issues, and discussions

**Mini Micro specific:**
- **Mini Micro resources:** https://miniscript.org/MiniMicro/#learn
- **Mini Micro Cheat Sheet:** https://miniscript.org/files/MiniMicro-CheatSheet.pdf
- **Built-in demos:** Mini Micro comes with example programs in `/sys/demo/` — load and study them:
  ```
  load "/sys/demo/ticTacToe"
  run
  ```

**Learning tips:**
- Start with the Mini Micro Cheat Sheet for basic and APIs
- Explore the `/sys/demo/` programs in Mini Micro to see working examples
- The wiki has pages for every built-in function with usage examples
- Use the interactive command line — type expressions directly to experiment

## String concatenation and mixing types

**User:** How do I combine strings and numbers together in MiniScript output?

**Assistant:** Use the `+` operator to concatenate strings and numbers. MiniScript automatically converts numbers to strings when you add them to a string:

```
name = "Alice"
age = 30
print "Hello, " + name + "! You are " + age + " years old."
// Hello, Alice! You are 30 years old.
```

The key rule: if either side of `+` is a string, the result is string concatenation. If both sides are numbers, it does addition.

```
print "Score: " + 42      // Score: 42 (string + number = concatenation)
print 10 + 20              // 30 (number + number = addition)
print "10" + 20            // 1020 (string + number = concatenation)
```

If you need to explicitly convert a number to a string, use `str`:

```
x = 42
s = str(x)
print s        // "42" (but it's a string now)
```

Use of `str` gives you explicit control, but usually `+` handles it automatically. Just make sure the left side of your first `+` is a string if you want concatenation:

```
x = 10
y = 20
print x + y             // 30 (both numbers, so addition)
print "" + x + y         // 1020 (starts with string, so concatenation)
print x + " and " + y    // 10 and 20 (string in the middle forces concatenation for the rest)
```

## String operators (subtraction and replication)

**User:** Can you subtract or multiply strings in MiniScript? What does that do?

**Assistant:** Yes! MiniScript supports several unusual but useful string operators.

**String subtraction (`-`):** Removes the right string from the end of the left string, if it exists.

```
print "banana" - "na"           // bana (removes "na" from the end)
print "abcabc" - "abc"          // abc (removes "abc")
print "myFile.txt" - ".txt"     // myFile (removes the ".txt" extension)
print "Hello World" - "o"       // Hello World (no change; string does not end in "o"
```

**String multiplication (`*`):** Repeats the string the given number of times:

```
print "ha" * 3          // hahaha
print "-" * 20          // --------------------
print "abc" * 0         // (empty string)
```

This is very handy for creating separators, padding, or repeated patterns:

```
print "=" * 40
print "  Title"
print "=" * 40
```

**String division (`/`):** Cuts a string down, just like multiplying by the inverse of the right-hand side.

```
print "banana" / 3         // "ba"
print "hello world!" / 2   // "hello "
```

## Order of operations

**User:** What order does MiniScript evaluate math operators, and how can I change it?

**Assistant:** MiniScript follows standard mathematical order of operations (precedence), from highest to lowest:

1. `^` — exponentiation (right-to-left)
2. `*`, `/`, `%` — multiplication, division, modulo
3. `+`, `-` — addition, subtraction
4. `<`, `>`, `<=`, `>=`, `==`, `!=` — comparisons
5. `not` — logical negation
6. `and` — logical AND
7. `or` — logical OR

**Examples:**

```
print 2 + 3 * 4       // 14 (not 20 — multiplication first)
print 10 - 3 + 2       // 9 (left-to-right for same precedence)
print 10 % 3 * 2       // 2 (modulo first: 10%3=1, then 1*2=2)
```

**Use parentheses to override precedence:**

```
print (2 + 3) * 4      // 20
print (10 - 3) + 2      // 9

// More practical example:
average = (a + b + c) / 3
```

**Tip:** When in doubt, use parentheses to explicitly group parts of an expression. They make your intent clear even if they're not strictly necessary:

```
// Both produce the same result, but the second is clearer:
result = a * b + c / d
result = (a * b) + (c / d)
```

## Calling functions with dot syntax

**User:** What's the difference between `len("Hello")` and `"Hello".len` in MiniScript?

**Assistant:** They do the same thing — both return `5`. MiniScript lets you call many built-in functions either way: as a traditional function call or using dot syntax.

```
s = "Hello"
print len(s)     // 5
print s.len      // 5
```

The dot syntax (`.len`) is generally preferred as more idiomatic MiniScript. It reads more naturally and chains well:

```
// Dot syntax (idiomatic):
myList = [1, 2, 3, 4, 5]
print myList.len       // 5
s = "Hello World"
print s.upper          // HELLO WORLD
print s.upper.indexOf("L")   // 2

// Function syntax (also works):
print len(myList)      // 5
print upper(s)         // HELLO WORLD
print indexOf(upper(s), "L")  // 2
```

Note that with dot syntax, the value before the dot becomes the "self" argument. So `s.indexOf("W")` is equivalent to `indexOf(s, "W")`.  This works only for functions where the first parameter is named "self".

This applies to many built-in functions: `len`, `val`, `str`, `code`, `char`, `indexOf`, `replace`, `split`, `join`, `upper`, `lower`, `trim`, `hasIndex`, `remove`, `push`, `pop`, `pull`, `sort`, `shuffle`, `sum`, `indexes`, `values`, and more.

**When you must use function syntax:**

For functions that don't operate on a specific value, like `rnd`, `time`, or `print`; and on most numeric functions, like `abs`, `cos`, or `floor`, you use the normal function call syntax:

```
print floor(3.7)    // 3
print rnd            // random number 0-1
```

## Generating random numbers

**User:** How do I generate a random integer between 1 and 100 in MiniScript?

**Assistant:** Use the `rnd` function with `floor`, and add one:

```
n = floor(rnd * 100) + 1
print n   // random integer from 1 to 100
```

How it works:
- `rnd` returns a random number from 0 (inclusive) to 1 (exclusive)
- Multiplying by 100 gives a range of 0 to 99.999...
- `floor` rounds down to the nearest integer, giving 0 to 99
- adding 1 bumps this into the desired range, 1 to 100

**General formula for a random integer from `a` to `b`:**

```
n = floor(rnd * (b - a + 1)) + a
```

Examples:

```
die = floor(rnd * 6) + 1         // 1 to 6 (die roll)
coin = floor(rnd * 2)            // 0 or 1 (coin flip)
percent = floor(rnd * 101)       // 0 to 100
```

**Picking a random element from a list:**

List indexing ignores the decimal part, doing `floor` implicitly.  So you can just do:

```
colors = ["red", "blue", "green", "yellow"]
pick = colors[rnd * colors.len]
print pick   // random color
```

**Other useful `rnd` patterns:**

```
// Random number with decimal places (e.g., 0.0 to 10.0):
x = rnd * 10

// 50% chance of something:
if rnd < 0.5 then print "heads" else print "tails"

// 20% chance:
if rnd < 0.2 then print "critical hit!"
```

## Including quotation marks in a string

**User:** How do I include quotation marks inside a MiniScript string?

**Assistant:** In MiniScript, you include a literal quote mark inside a string by doubling it — use `""` inside the string:

```
print "She said ""hello"" to me."
// Output: She said "hello" to me.
```

A few more examples:

```
quote = "The sign read ""DO NOT ENTER""."
print quote
// Output: The sign read "DO NOT ENTER".

dialog = "He asked, ""How are you?"""
print dialog
// Output: He asked, "How are you?"
```

MiniScript does **not** use backslash escapes like `\"` — that's a common mistake if you're coming from Python, JavaScript, or C. The only escape-like mechanism is doubling the quote character.

**Special characters:**

For other special characters like newlines or tabs, use the `char` function with the Unicode code point:

```
newline = char(10)
tab = char(9)
print "Line 1" + newline + "Line 2"
// Output:
// Line 1
// Line 2

print "Col1" + tab + "Col2"
// Output: Col1	Col2
```

## The `print` command

**User:** How do I display output in MiniScript?

**Assistant:** Use the `print` command:

```
print "Hello, world!"
print 42
print 2 + 3    // prints 5
```

`print` outputs a value followed by a newline. It can print any type:

```
print [1, 2, 3]                  // [1, 2, 3]
print {"name": "Alice"}          // {"name": "Alice"}
print null                       // null
print true                       // 1
```

**Printing without a newline:** `print` takes a second parameter, which is the separator to print after the given string.  By default this is a newline, but you can specify anything else, including an empty string if you just want to suppress the newline.

```
for i in range(1, 5)
    print i, ""
end for
print "!"
// Output: 12345!
```

**Printing multiple values:** Concatenate them with `+`:

```
name = "Alice"
score = 95
print name + " scored " + score + " points"
// Alice scored 95 points
```

Or, if you need to use multiple `print` calls (e.g. because you are iterating over some collection), use the second parameter as in the previous example.

**Note:** Parentheses are not needed (and discouraged) around the argument to `print`:

```
print "Hello"      // good (idiomatic)
print("Hello")     // works, but unnecessary parens
```

## Case sensitivity

**User:** I wrote `Print "hello"` and got an "Undefined Identifier" error. What went wrong?

**Assistant:** MiniScript is case-sensitive. The correct command is `print` (all lowercase), not `Print`:

```
Print "hello"   // ERROR: Undefined Identifier: 'Print'
print "hello"   // correct!
```

This applies to all keywords and built-in functions in MiniScript — they are all lowercase:

```
// Wrong (capital letters):
For i In Range(1, 5)    // errors!
If x > 5 Then           // errors!
While True              // errors!

// Correct (all lowercase):
for i in range(1, 5)    // good
if x > 5 then           // good
while true              // good
```

The same goes for built-in functions like `floor`, `ceil`, `abs`, `rnd`, `str`, `val`, `len`, etc. — always lowercase.

Your own variable and function names can use any mix of cases:

```
myScore = 100       // fine
PlayerName = "Ada"  // fine (but camelCase is more conventional)
```

If you get an "Undefined Identifier" error, check the capitalization first — it's one of the most common mistakes.

## Numbers and exponential notation

**User:** How do I write very large or very small numbers in MiniScript?

**Assistant:** MiniScript supports scientific notation using `e` or `E`:

```
bigNum = 3.5e6       // 3,500,000
smallNum = 2.1e-8    // 0.000000021

print bigNum         // 3500000
print smallNum       // 2.1E-08
```

The `e` means "times 10 to the power of":
- `1e3` = 1 × 10³ = 1000
- `5e-4` = 5 × 10⁻⁴ = 0.0005
- `6.022e23` = Avogadro's number

**Examples:**

```
speedOfLight = 3e8       // 300,000,000 m/s
electronMass = 9.109e-31  // kg
million = 1e6
billion = 1e9
```

MiniScript uses double-precision floating point numbers, which gives you about 15-17 significant digits and a range of roughly ±1.8e308.

**Converting strings with scientific notation:**

```
s = "3.5e6"
print s.val    // 3500000
```

The `val` function handles scientific notation in strings automatically.

## Strings vs. numbers

**User:** What's the difference between `print 42` and `print "42"` in MiniScript?

**Assistant:** Both display `42` on screen, but the values are different types:

- `42` is a **number** — you can do math with it
- `"42"` is a **string** — a sequence of characters

The difference matters when you use operators:

```
print 42 + 8       // 50 (numeric addition)
print "42" + 8     // 428 (string concatenation)

print 42 * 2       // 84 (multiplication)
print "42" * 2     // 4242 (string replication)
```

**Converting between them:**

```
// String to number:
n = "42".val       // 42 (as a number)
print n + 8        // 50

// Number to string:
s = str(42)        // "42" (as a string)
print s + "!"      // 42!
```

**Checking the type:**

```
print 42 isa number     // 1 (true)
print "42" isa number   // 0 (false)
print "42" isa string   // 1 (true)
```

This distinction is especially important with `input`, which always returns a string:

```
x = input("Enter a number: ")     // x is a STRING
print x + 10                      // concatenates! ("510" if you typed 5)
print x.val + 10                  // adds! (15 if you typed 5)
```

