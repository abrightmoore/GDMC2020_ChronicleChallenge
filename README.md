# GDMC2020_ChronicleChallenge

Simulated agents wander the landscape. They construct buildings based on the type of materials within the local area as well as using their own artistic style. Occasionally agents will make a new child who inherits artistic characteristics from the parent.

![City](https://pbs.twimg.com/media/Ead3ly8VcAAn0jT?format=jpg&name=large)

Procedural Settlement Generation. See https://twitter.com/GenDesignMC for details of the challenge

You can review by development notes for 2020 on Twitter here: https://twitter.com/abrightmoore/status/1271037719431409669?s=20

You can check out my 2019 effort here: https://github.com/abrightmoore/ProceduralSettlementsInMinecraft
You can read about my experience here: http://www.brightmoore.net/what-s-happening-now/gdmc2019-proceduralsettlementgenerationinminecraftround2

You can check out my 2018 effort here: http://www.brightmoore.net/mcedit-filters-1/abode
You can read about my experience here: http://www.brightmoore.net/what-s-happening-now/gdmc2018competition-aparticipantsperspective

# MY APPROACH

In this year's effort, I use autonomous agents to roam the selected landscape and build structures that use materials from the local environment.

Each agent has a distinctive material and pattern style which is reflected in their structures. Agents are also capable of coming together to create a child that inherits the design aesthetic of their parents. To celebrate this act of creation, a tree appears in the landscape with a design merged from the two parents and the child.

# SELECTED ASPECTS OF THE GENERATED SETTLEMENT

Houses are multistorey clusters of rooms randomly stacked. Struts are used to connect overhanging parts with the ground, suggesting force carrying pillars. This approach solved the problem of dealing with terrain variation. In past years I was profiling the gradient of the land looking for building plots that were suitably slightly sloping. This year I allow the agent to build clusters of dwellings where they like, regardless of the severity of terrain. It is quite effective at dealing with structure placement.

The type of dwelling and style of dwelling plot is determined by the resources found within the landscape. Before building, the landscape columns are sampled at intervals and the resulting materials of interest are indexed for later access by the agents:

* Water allows farms
* Woods allow cottages
* Lava permits blacksmith, which is a very large cottage plot currently.
* Ore resources permit vertical mineshafts, with an industrial set of buildings above ground and a mine head building on top.
* Stone allows ancient crumbling structures (which can also be built upon in later simulation iterations), castle-like forts, round towers, or mystrious impenetrable wizards spires.
* An occasional stone path section is placed showing the areas that agents have wandered through.

There is also a central hub platform in the settlement which hosts a ramshackle tower, as well as the names of selected agents that have built out the settlement on signs. This is intended to mimic the special spawn area in shared online servers.

The wall sections of buildings are patterned according to a spatial field unique to each agent. As you trace through the village you will see similar structure colours used in similar ways by the same 'person'.

As each dwelling is built, an array of rooms is returned from the heirarchical generator which are intended to be used in populating the interiors. The interiors have been 'dressed' with functional blocks where appropriate, and doors added. As these are all private residences, access is not always convenient for the casual interloper - consider leaving people to their privacy.

# THE CHRONICLE CHALLENGE

One optional challenge is to provide lore in the world to enhance the experience of the settlement. In my solution I track events as the simulation unfolds and then report them in chronological order on the MCEdit console output at the end of the simulation attempt.

As part of my response to the Chronicle challence, ingame signs are used to show which agent is responsible for the dwellings and structures they build. A list of named signs at the settlement hub are used to invoke the experience of exploring a well-played shared world.

Seek out the chest on the corner of the central hub. Within is the settlement almanac, consisting of the settlement name, and details of all the 'builders' who contributed to it. Within the almanac is the last known location of each builder. At that location you will find a personal diary, though you will need to desecrate the grave to read it! As an additional challenge, the graves may be haunted by the spirit of the dead...

![Farms and cottages](https://pbs.twimg.com/media/EadN7evUcAAVaGK?format=jpg&name=large)

![Settlement Example - Birch Wood](https://pbs.twimg.com/media/EabpICeU0AYOVVA?format=jpg&name=large)

![Settlement Example - Oak Wood](https://pbs.twimg.com/media/EabjEnJUwAEKa_a?format=jpg&name=large)

![Chronicle elements ingame](https://pbs.twimg.com/media/EabynwOUEAUpFqD?format=png&name=900x900)
