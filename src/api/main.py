import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from api.runeterra_map_api import RuneterraMapAPI

RuneterraMapAPI.fetch_universe_meeps()
RuneterraMapAPI.fetch_content_panel()
RuneterraMapAPI.fetch_content_panel(is_card=True)
