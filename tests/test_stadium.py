from ursinaxball.common_values import BaseMap
from ursinaxball.objects import load_stadium_hbs


def test_stadium():
    stadium = load_stadium_hbs(BaseMap.CLASSIC)
    assert stadium.name == "Classic"


def test_traits():
    """Test that traits are correctly applied to the discs in the stadium."""
    stadium = load_stadium_hbs(BaseMap.CLASSIC)

    # Classic map has two goals
    assert len(stadium.goals) == 2

    # Find goal post discs
    goal_posts = [disc for disc in stadium.discs if disc.trait == "goalPost"]
    assert len(goal_posts) == 4  # Two posts per goal

    # Check if each post has a invMass of 0
    inv_mass = [disc.inverse_mass == 0 for disc in goal_posts]
    assert inv_mass.count(True) == 4
