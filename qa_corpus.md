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
