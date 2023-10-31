import pytest
from unittest.mock import Mock
from main import share_knowledge

@pytest.mark.parametrize(
    "player_location, player_hand, other_players, expected_output, expected_card_transfer",
    [
        # Test case 1: Happy path, player can give card
        ("Paris", ["Paris"], [Mock(get_location=Mock(return_value="Paris"), get_hand=Mock(return_value=[]))], "Paris given to", True),
        # Test case 2: Happy path, player can take card
        ("London", [], [Mock(get_location=Mock(return_value="London"), get_hand=Mock(return_value=["London"]))], "You received London from", True),
        # Test case 3: Edge case, no other players in location
        ("Berlin", ["Berlin"], [], "There is no one else in your location", False),
        # Test case 4: Error case, player can't share knowledge
        ("Madrid", [], [Mock(get_location=Mock(return_value="Madrid"), get_hand=Mock(return_value=[]))], "You can't share knowledge with anyone", False),
    ],
    ids=["happy_path_give", "happy_path_take", "edge_no_players", "error_no_share"]
)
def test_share_knowledge(monkeypatch, player_location, player_hand, other_players, expected_output, expected_card_transfer):
    # Arrange
    player = Mock(get_location=Mock(return_value=player_location), get_hand=Mock(return_value=player_hand), add_card=Mock())
    monkeypatch.setattr('builtins.input', lambda _: 0)
    self = Mock(players=[player] + other_players, available_players=other_players)

    # Act
    share_knowledge(self, player)

    # Assert
    if expected_card_transfer:
        player.add_card.assert_called_once()
    else:
        player.add_card.assert_not_called()
    assert expected_output in capsys.readouterr().out
