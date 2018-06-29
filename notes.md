# Databases and Machine Learning

## Introduction to Self-Driving DBs - [CMU Article](http://www.cs.cmu.edu/~pavlo/blog/2018/04/what-is-a-self-driving-database-management-system.html)

Using ML to automate a DB's runtime operations and physical design is a hot research topic. This new class of DBs are called self-driving DBs. Example, [Peloton](https://pelotondb.io/) created by Andy Pavlo at CMU. 

### Self-Adaptive DBs (1970s-1990s)

The idea of using a DBMS to remove the burden of data management from application developers was one of the original selling points of the relational model and declarative programming languages (e.g., SQL) from the 1970s. With this approach, a developer only writes a query that specifies what data they want to access. It is then up to the DBMS to find the most efficient way to execute that query; the developer does not worry about what algorithm to use, how to store and retrieve data, or how to safely interleave operations that update data.  The DBMS knows the most about the database and how it is accessed, so therefore it is always in the best position to make these decisions.

In this same vein, organizations ideally want a DBMS to pick an overall strategy for their application that handles all aspects of managing and optimizing their database. These were called self-adaptive systems in the 1970s. The high-level idea of how these early systems worked is essentially how modern tools work today: (1) the system collects metrics on how the application accesses data and then (2) it searches for what change to make to improve performance based on a cost model.

The early self-adaptive DBMSs focused on physical database design, in particular index selection. Index Selection: Given a workload consisting of SQL statements on a database, and a user-specified storage constraint, recommend a set of indexes that have the maximum benefit for the given workload. Index: An index is a copy of selected columns of data from a table that can be searched very efficiently that also includes a low-level disk block address or direct link to the complete row of data it was copied from.

Another database design problem was database partitioning. Database Partitioning: Partitioning is the database process where very large tables are divided into multiple smaller parts. By splitting a large table into smaller, individual tables, queries that access only a fraction of the data can run faster because there is less data to scan.

### Self-Tuning DBs (1990s-2000s)

At the forefront of the self-tuning DB movement was the seminal work at Microsoft Research with the AutoAdmin project. They built advisor tools that helped the DBA select the optimal indexes, materialized views (Materialized Views: In computing, a materialized view is a database object that contains the results of a query. For example, it may be a local copy of data located remotely, or may be a subset of the rows and/or columns of a table or join result, or may be a summary using an aggregate function. You keep a materialized view to be able to access that information easily if the creation of that "view" is a common task for the DB.), and partitioning schemes for their workload. The key contribution from AutoAdmin was the development of the what-if API. With this, the tuning tools create virtual catalog entries for potential design decisions (e.g., an index to add) and then use the query optimizer's cost model to determine the benefit of that decision. In other words, you tell the optimizer that the database has an index even though it really does not, and then see if the optimizer selects that index for each query to determine whether adding that index is a good idea. Essentially if the optimizer thinks the query is a good idea then the cost should decrease over a large set of queries that are representative of the query load of the system. . This allows the tools to use the existing DBMS's cost model estimates rather than having to create a second external (and therefore likely inaccurate) cost model to make design decisions. The other major database vendors had similar self-tuning physical design projects (e.g., IBM's DB2 Designer), but Microsoft was the most prolific.

The 2000s also saw the beginning of research on automating knob configuration. Such knobs allow the DBA to control various aspects of the DBMS's run-time behavior. For example, they can set how much memory the system allocates for data caching versus the transaction log (A transaction log is a sequential record of all changes made to the database while the actual data is contained in a separate file. The transaction log contains enough information to undo all changes made to the data file as part of any individual transaction.) buffer. Unlike physical design tools, configuration tools cannot use the built-in cost models of query optimizers. This is because these models generate estimates on the amount of work to execute a particular query and are intended to compare alternative query execution strategies in a fixed execution environment. IBM released a version of DB2 with a self-tuning memory manager that uses heuristics to determine how to allocate the DBMS's memory to its internal components. Using all of the above tools is still a manual process: the DBA provides a sample workload and then the tool suggests one or more actions to improve performance. It is still up to the DBA to decide whether those suggestions are correct and when to deploy them. IBM recognized that requiring a human expert to make these final decisions was problematic, thus they launched an initiative on building autonomic components for DB2. The basic idea is simple: the DBMS's cost model makes estimations when selecting a query plan based on statistics that it collects. Then as the system executes the query, it checks whether those estimates match with the real data. If not, then the system has a feedback loop mechanism to provide the cost model with corrections. This seems like exactly what one would want in a system, but I have yet to meet any DB2 DBA that says that it worked as advertised. I have been told by at least three DBAs that they always turn off this feature whenever they first deployed a new DB2 database. The idea of removing the need for humans has also been explored for some aspects of physical design. Most notable is the great database cracking (Database Cracking is an incremental partial indexing and/or sorting of the data.)work from Stratos Ideros.

### Cloud DBs (early 2010s)

The next chapter in autonomous systems came about with the rise of cloud computing. Automation is more necessary in such cloud platforms because of their scale and complexity. All of the cloud providers use custom tools to control deployments at the operator-level (e.g., tenant placement). Microsoft appears to be again leading research in this area. Their Azure service models resource utilization of DBMS containers from internal telemetry data and automatically adjusts allocations to meet QoS and budget constraints. I have not seen or heard of anything with the same level of sophistication from the other cloud database vendors. 

There were a lot of cloud specific terms and jargon that might not be immediately relevant. So there are no more notes on the cloud.

### Self-Driving DBs (late 2010s)

Term derived from self-driving cars (of course!). Here is a formal definition: 

* The ability to automatically select actions to improve some objective function (e.g., throughput, latency, cost). This selection also includes how many resources to use to apply an action.

* The ability to automatically choose when to apply an action.

* The ability to learn from its actions and refine its decision making process.

Now let us define what an action in the above meant: : (1) a change to the database's physical design (e.g., add/drop an index), (2) a change to the DBMS's knob configuration (e.g., allocate more/less memory to the DBMS's log buffer), or (3) a change to the DBMS's physical resources (e.g., add/remove a node in the cluster). The problem choosing how to apply an action is part of the action selection process. For example, the DBMS could choose to build a new index using one thread if resources are limited, or it could choose to use four threads if it needs to build that index more quickly. 

 With a few exceptions, all of the previous work is focused on solving the first problem. There are a few tools that attempt to solve part of the second problem and to the best of my knowledge nobody has solved the last one. But these are what make a self-driving DBMS difficult. The DBMS must know when it should do deploy an action and whether that action helped. This is more than identifying that Sunday morning is when demand is low so therefore the system can optimize itself more aggressively. The system must have a sense of what the workload will look like in the future and plan accordingly. Without this forecasting, the DBMS is equivalent to a self-driving car that is only able to view the road behind it. The car can see all of the children that it ran over in the past but it is not able to predict the future children and avoid them in the road ahead.

### Other Projects

1. Deep Tune DB — Jens Dittrich and his team at Saarland University are exploring the use of RL for physical design. They have a proof-of-concept for index selection. Jens also had a previous project, called OctopusDB, that supported hybrid storage models and was influential to the design of our storage manager.

2. CrimsonDB — This is also a newer project from Stratos Ideros' group at Harvard. It is part of his larger theme on self-designing systems. The main idea is that the DBMS can optimize its physical data structures according to changes in the workload and hardware.

3. DBSeer — This is an external framework from Barzan Mozafari's group in Michigan. It helps a DBA diagnose problems by comparing regions in the DBMS's performance time-series data where the system was slow with regions where it behaved normally. These techniques could be used for estimating the benefit/cost of actions in a self-driving planner. Barzan also has a great VLDB'17 paper on adaptive lock scheduling for MySQL.

## Our Project

The primary goal of our project would be to decide on which materialized views (MV) and indices (together referred to as physical design structures) to create, given the amount of memory available (this is our space constraint), and given the fact that queries are not known in advance - hence the system needs to be dynamic – e.g. to drop some useless MVs and create new MVs depending on how the workload sequence evolves over time. Thus, the optimization problem here is: Given the space constraint of S, create the set of MVs and indices that will maximize the overall performance (minimize the cumulative response time) of workload W, assuming that the workload W (the set of queries belonging to W) is not known in advance. 

Some elaboration:

* Which Materialized views and indices to create. This might be thought of as two separate problems:
  1. If a set of rows get accessed a lot then should they be indices?
  2. If a view (collection of rows) gets created a lot through joins or other queries then should they be stored on disk to speed up processing.
  All of this is of course under the given the space constraints (S).
* Dynamic system - must find a good set of MVs and indices for a initial workload and must also evolve as the workload evolves.
* Objective - Reduce the cumulative response time of the workload W.
* Reinforcement Learning and Bandit Algorithms can help achieve this. These differ from supervised learning, in that the learner doesn’t just make predictions, but also can choose actions to take thereby changing what it will observe (and learn from) in the future. 

## Bandit Algorithms (*bandits* or MAB)

### [Wikipedia](https://en.wikipedia.org/wiki/Multi-armed_bandit)

The multiarm bandit problem is a problem in which a fixed limited set of resources must be allocated between competing (alternative) choices in a way that maximizes their expected gain when each choice's properties are only partially known at the time of allocation, and may become better understood as time passes or by allocating resources to the choice.

One-armed bandits - Row of slot machines where a gambler has to decide which machines to play, how many times to play each machine and in which order to play them, and whether to continue with the current machine or try a different machine. The multi-arm bandit problem falls into the broad category of Stochastic Scheduling.

In the problem, each machine provides a random reward from a probability distribution specific to that machine. The objective of the gambler is to maximize the sum of rewards earned through a sequence of lever pulls. The crucial tradeoff the gambler faces at each trial is between "exploitation" of the machine that has the highest expected payoff and "exploration" to get more information about the expected payoffs of the other machines. The trade-off between exploration and exploitation is also faced in reinforcement learning. In practice, multi-armed bandits have been used to model problems such as managing research projects in a large organization like a science foundation or a pharmaceutical company. In early versions of the problem, the gambler begins with no initial knowledge about the machines.


The multi-armed bandit problem models an agent that simultaneously attempts to acquire new knowledge (called "exploration") and optimize his or her decisions based on existing knowledge (called "exploitation"). The agent attempts to balance these competing tasks in order to maximize his total value over the period of time considered.

- [] Add Mathematical description of MABs from Wikipedia for easy access.

### [University of Maryland](http://www.cs.umd.edu/~slivkins/CMSC858G-fall16/Lecture2_PartI.pdf)

Covers mutli-arm bandits with independent and identically distributed rewards. The learner selects an arm from the list of arms at each time step as the learning progresses (Note: arms and actions used interchangably in this lecture). After taking action a_t at timestep t a reward for this action is realised and observed by the algorithm. The Horizon is the amount of time the process is going to go on for. The process is repeated until the end of the time-horizon is reached. Goal: Gather as much cumulative reward as possible.

It’s important to emphasize that the algorithm observes only the reward for the selected action, not all the other actions that could have been selected, that is why it is called a bandit feedback setting. The rewards for each action are independent of all the other actions and they are identically distributed for all actions (which means the probability of a reward r is the same for each arm?). The rewards are assumed to be in the range [0, 1]. Every time this action is chosen, the reward is sampled independently from this distribution. It is crucial that this distribution is unknown to the algorithm, and does not change over time.

The lecture also gives a nice set of examples which might be useful in explaining Bandit Algorithms to someone who might not know anything about them.

The notion of reward here is the use of regret. Maximise reward -> minimize regret. Regret is just the difference between the expected reward from the best arm and the average reward accumulated thus far by the algorithm. This is called regret because if shows how much the algorithm regrets not knowing what the best arm was. The regret given previously is expected regret and not realized regret. It might not make much sense to talk about realized regret because of the fact that. Different types of regret criterion.

- [] Add maths here.
- [] Clearly re-read the last section on regret.
- [] Read section 4.

### [ICML Tutorial on *bandits*](https://sites.google.com/site/banditstutorial/)

Here the user/player is called a forecaster. Forecaster chooses an arm (only one arm) and the reward for only that arm is displayed to the forecaster.

The enviromnet can be stochastic or adversarial.


### Possible Issues

1. Bandits assume that the underlying distribution of the rewards doesn't change over time. In a databbase I would imagine that the distribution of rewards and even the range would change over time.
2. Rewards from changing the same knob will be the same if the conditions are assumed to be the same over a long period of time.

## Similar Work

### [The Case for Automatic Database Administration using Deep Reinforcement Learning](https://arxiv.org/pdf/1801.05643.pdf)

DBMS is a large and complex piece of software. It has lead to the job of a DBA. DBAs tend to use experience and intuition as much as they use the database advisory tools that different vendors seem to pack along with their DBMS. Since both intution and experience are deeply embedded into the field of ML it makes sense to try to teach a ML model to do the job of a DB admin. More specfically Deep Reinforcement Learning has proved to be an interesting candidate for problems with really large search spaces and complex problems.

#### Deep Reinforcement Learning

Deep Reinforcement Learning does not require any expected outputs. The training is completely driven by so called rewards, that tell thelearner whether a taken action lead to a positive or a negative result on the input. Dependingon the outcome, the neural network is encouraged or discouraged to consider the action on this input in the future.

#### Usage

Input are a set of queries and the current configuration of the database in terms of the indexes. 

#### Ideas from paper

1. There should exist a drop function. It will allow for a configuration that makes a lot more sense (Not sure if this was not done due to complexity). Possible model. Example model:
  * If n (number of indices) = 0, the possible operation add_index() (with the hope that indexing makes something better)
  * If n > 0 and n < k then possible actions: add_index() and drop_index() or add_index
  * If n = k  possible action: add_index() and drop_index().
  Can even remove the dropping from 2. if too complex to do.




