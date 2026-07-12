"""
Contains every event enum.

Example
    EventType.USER_MESSAGE

    EventType.ACTION_PLANNED

    EventType.TOOL_COMPLETED

    EventType.WORLD_UPDATED

    EventType.ACTION_VERIFIED

    EventType.RETRY_ACTION

"""

from enum import Enum


class EventTypes(Enum):
    """
    Event exchanged between agent components.

    Each event represents something that happened in
    the agent and can be published through the EventBus.

    """

    # ^ ============================================
    # ^ Agent Lifecycle
    # ^ ============================================

    AGENT_STARTED='agent_started'
    AGENT_STOPPED="agent_stopped"

    GOAL_STARTED="goal_started"
    GOAL_COMPLETED="goal_completed"
    GOAL_FAILED="goal_failed"

    # ^ ============================================
    # ^ Conversation
    # ^ ============================================

    USER_MESSAGE="user_message"
    AGENT_MESSAGE="agent_message"


    ASK_USER='ask_user'
    USER_RESPONSE='user_response'

    CONFIRMATION_REQUIRED='confirmation_required'
    USER_CONFIRMED='user_confirmed'
    USER_CANCELLED='user_cancelled'

    # ^ ============================================
    # ^ Planning
    # ^ ============================================

    PLAN_STARTED='plan_started'
    ACTION_PLANNED="action_planned"
    PLAN_COMPLETED='plan_completed'
    PLAN_FAILED='plan_failed'

    REPLAN_REQUIRED='replan_required'



    # ^ ============================================
    # ^ Execution
    # ^ ============================================

    ACTION_STARTED = "action_started"

    TOOL_SELECTED = "tool_selected"

    TOOL_EXECUTING = "tool_executing"

    TOOL_COMPLETED = "tool_completed"

    TOOL_FAILED = "tool_failed"

    
    #^ ==========================================================
    #^ Observation
    #^ ==========================================================

    WORLD_UPDATED = "world_updated"


    #^ ==========================================================
    #^ Recovery
    #^ ==========================================================

    RECOVERY_STARTED = "recovery_started"

    RETRY_ACTION = "retry_action"

    USE_FALLBACK = "use_fallback"

    ASK_HUMAN = "ask_human"

    ABORT_TASK = "abort_task"

    RECOVERY_COMPLETED = "recovery_completed"



    #^ ==========================================================
    #^ Memory
    #^ ==========================================================

    MEMORY_READ = "memory_read"

    MEMORY_UPDATED = "memory_updated"

    MEMORY_WRITTEN = "memory_written"

    MEMORY_SUMMARIZED = "memory_summarized"



    #^ ==========================================================
    #^ Context
    #^ ==========================================================

    CONTEXT_BUILDING = "context_building"

    CONTEXT_READY = "context_ready"






