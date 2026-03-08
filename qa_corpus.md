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

The loop variable (`kv`) is a mini-map with `.key` and `.value` properties for each entry.

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
