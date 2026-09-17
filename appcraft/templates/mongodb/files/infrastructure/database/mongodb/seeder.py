from __future__ import annotations

from typing import TYPE_CHECKING, Any

from domain.models.programmer import NewProgrammer, Programmer

if TYPE_CHECKING:
    from infrastructure.database.mongodb.adapter import MongoDBAdapter


class ProgrammerSeeder:
    """Seeds the 'programmers' collection with a handful of open-source
    community figures — a runnable example of MongoDBAdapter.create()
    against a real document model (see runners/tools/programmers.py).
    """

    def __init__(self, adapter: MongoDBAdapter):
        self.adapter = adapter

    def seed(self) -> None:
        if self.adapter.get(Programmer):
            return

        for data in self._programmers():
            self.adapter.create(Programmer, NewProgrammer(**data))

    def _programmers(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "Thiago Pereira",
                "country": "Brazil",
                "technologies": [
                    "Python",
                    "PHP",
                    "TypeScript",
                    "JavaScript",
                ],
                "main_projects": ["AppCraft", "SOAD", "ModulePHP"],
                "bio": (
                    "Creator of AppCraft, a Clean Architecture project "
                    "scaffolding and template CLI for Python, among "
                    "other open-source projects."
                ),
            },
            {
                "name": "Richard Stallman",
                "country": "United States",
                "technologies": ["C", "Lisp", "Emacs Lisp"],
                "main_projects": [
                    "GNU Project",
                    "GCC",
                    "Emacs",
                    "GDB",
                    "GNU General Public License",
                ],
                "bio": (
                    "Founder of the GNU Project and the Free Software "
                    "Foundation; author of the GPL and one of the "
                    "original architects of the free software movement."
                ),
            },
            {
                "name": "Linus Torvalds",
                "country": "Finland",
                "technologies": ["C"],
                "main_projects": ["Linux kernel", "Git", "Subsurface"],
                "bio": (
                    "Creator of the Linux kernel and of Git, the "
                    "distributed version control system used by most "
                    "of the open-source world today."
                ),
            },
            {
                "name": "Guido van Rossum",
                "country": "Netherlands",
                "technologies": ["Python", "C"],
                "main_projects": ["Python", "CPython"],
                "bio": (
                    "Creator of Python; served as the language's "
                    "'Benevolent Dictator For Life' until 2018. Worked "
                    "at Google, Dropbox and Microsoft."
                ),
            },
            {
                "name": "Ken Thompson",
                "country": "United States",
                "technologies": ["B", "C", "Go"],
                "main_projects": ["Unix", "B language", "Go", "UTF-8"],
                "bio": (
                    "Co-created Unix and the B language (C's "
                    "predecessor) with Dennis Ritchie at Bell Labs, "
                    "and decades later co-created Go at Google."
                ),
            },
            {
                "name": "Yukihiro Matsumoto",
                "country": "Japan",
                "technologies": ["Ruby", "C"],
                "main_projects": ["Ruby"],
                "bio": (
                    "Known as 'Matz'; creator of the Ruby programming "
                    "language, designed to make programming more "
                    "enjoyable for developers."
                ),
            },
            {
                "name": "Brendan Eich",
                "country": "United States",
                "technologies": ["JavaScript", "C++"],
                "main_projects": ["JavaScript", "Mozilla Firefox", "Brave"],
                "bio": (
                    "Created JavaScript in 10 days at Netscape; "
                    "co-founded Mozilla and later Brave Software."
                ),
            },
        ]
