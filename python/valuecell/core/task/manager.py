import asyncio
from datetime import datetime
from typing import Dict

from .models import Task, TaskStatus


class TaskManager:
    """Lightweight in-memory task manager.

    Simplified to remove pluggable stores. If persistence is needed later,
    a thin adapter can wrap these methods.
    """

    def __init__(self):
        # In-memory store keyed by task_id
        self._tasks: Dict[str, Task] = {}
        # Process-local concurrency guard; protects in-memory state
        self._lock = asyncio.Lock()

    # ---- basic registration ----

    async def update_task(self, task: Task) -> None:
        """Update task"""
        async with self._lock:
            # Explicit updates should refresh updated_at
            task.updated_at = datetime.now()
            self._update_task_no_lock(task)

    def _update_task_no_lock(self, task: Task) -> None:
        """Write task to store without modifying timestamps.

        Callers must hold `_lock` before invoking this method.
        """
        self._tasks[task.task_id] = task

    # ---- internal helpers ----
    def _get_task(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    # Task status management
    async def start_task(self, task_id: str) -> bool:
        """Start task execution"""
        async with self._lock:
            task = self._get_task(task_id)
            if not task or task.status != TaskStatus.PENDING:
                return False

            task.start()
            self._update_task_no_lock(task)
            return True

    async def complete_task(self, task_id: str) -> bool:
        """Complete task"""
        async with self._lock:
            task = self._get_task(task_id)
            if not task or task.is_finished():
                return False

            task.complete()
            self._update_task_no_lock(task)
            return True

    async def fail_task(self, task_id: str, error_message: str) -> bool:
        """Mark task as failed"""
        async with self._lock:
            task = self._get_task(task_id)
            if not task or task.is_finished():
                return False

            task.fail(error_message)
            self._update_task_no_lock(task)
            return True

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel task"""
        async with self._lock:
            task = self._get_task(task_id)
            if not task or task.is_finished():
                return False

            task.cancel()
            self._update_task_no_lock(task)
            return True

    # Batch operations
    async def cancel_conversation_tasks(self, conversation_id: str) -> int:
        """Cancel all unfinished tasks in a conversation"""
        async with self._lock:
            tasks = [
                t for t in self._tasks.values() if t.conversation_id == conversation_id
            ]
            cancelled_count = 0

            for task in tasks:
                if not task.is_finished():
                    task.cancel()
                    self._update_task_no_lock(task)
                    cancelled_count += 1

            return cancelled_count
