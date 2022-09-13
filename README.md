# Wedding Seat Optimiser using Gurobi MILP Solver.
Using a CSV file or manual input, user can input relationships between guests. These will then be used to give optimal solution.

# Build & Run

First input your WLS License details into the relevant json, then:

```
$ docker build -t wedding-seat .      
$ docker run -p 8080:8080 wedding-seat
```
