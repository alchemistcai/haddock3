"""HADDOCK3 library."""
import logging
import sys
from pathlib import Path


log = logging.getLogger(__name__)
log.handlers.clear()
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s %(module)s %(levelname)s] %(message)s"))
log.addHandler(handler)

haddock3_source_path = Path(__file__).resolve().parent
haddock3_repository_path = haddock3_source_path.parents[1]
core_path = Path(haddock3_source_path, "core")
toppar_path = Path(haddock3_source_path, "cns", "toppar")
modules_defaults_path = Path(haddock3_source_path, "modules", "defaults.yaml")

FCC_path = Path(haddock3_source_path.parent, 'fcc')

config_expert_levels = ("easy", "expert", "guru")
# yaml parameters with this `explevel` should be ignored when reading the yaml
_hidden_level = "hidden"


class EmptyPath:
    """Define the type EmptyPath."""

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    def __bool__(self):
        return False


# version
version = "3.0.0"
v_major, v_minor, v_patch = version.split('.')

contact_us = 'https://github.com/haddocking/haddock3/issues'
