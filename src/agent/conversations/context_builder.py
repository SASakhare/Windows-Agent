'''
Planner shouldn't know:

    How to build prompts
    Which memories to retrieve
    Which messages to include
    Which tools to expose
    Which world state matters

    
Context Builder creates

    Goal

    Current Step

    Relevant Memory

    Recent Messages

    Current World

    Available Tools

    Instructions

Planner never builds prompts.
'''