"""Mold prefill values."""
import json

from ..config import load_prefilled, prefill_file
from ..hook import _domains
from .generate import gather_interfaces, dialog


def prefill_show():
    """Show prefilled values."""
    values = load_prefilled()
    if not values:
        print('No prefilled values!')
        return

    for k, v in values.items():
        print(f'{k}: {v}')


def prefill_clear():
    """Clear prefilled values."""
    prefill_file.unlink(missing_ok=True)


def prefill_fill():
    """Prefill values."""
    faces = set()
    for domain in _domains:
        faces.update(set(gather_interfaces(domain.tools)))

    questions = [q for face in faces for q in face.questions if q.prefill]
    for question in questions:
        question.response = dialog(question.prompt)

    values = {question.id: question.response for question in questions}

    prefill_file.parent.mkdir(parents=True, exist_ok=True)
    prefill_file.write_text(json.dumps(values, indent=4, sort_keys=True))
