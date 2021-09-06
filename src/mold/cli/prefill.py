"""Mold prefill values."""
import json

from ..config import user_configs
from ..hook import _domains
from .generate import gather_interfaces, dialog

prefill_file = user_configs / 'prefill.json'


def prefill_show():
    """Show prefilled values."""
    if not prefill_file.exists():
        print('No prefilled values!')
        return

    values = json.loads(prefill_file.read_text())
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
