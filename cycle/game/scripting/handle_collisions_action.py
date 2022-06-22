#from itertools import cycle
import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the Cyclist collides
    with the food, or the Cyclist collides with its segments, or the Cyclist collides with the opposing player, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._points = 0

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_food_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_food_collision(self, cast):
        """Updates the score nd moves the food if the Cyclist collides with the food.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        score1, score2 = cast.get_actors("scores")
        food = cast.get_first_actor("foods")
        cycles = cast.get_actors("cycles")
        if not self._is_game_over:
            cycle1 = cycles[0]
            cycle2 = cycles[1]
        head1 = cycle1.get_segments()[0]
        head2 = cycle2.get_segments()[0]

        if head1.get_position().equals(food.get_position()):
            points = food.get_points()
            score1.add_points(points)
            food.reset()
        elif head2.get_position().equals(food.get_position()):
            points = food.get_points()
            score2.add_points(points)
            food.reset()

    
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the Cyclist collides with one of its segments or the opposing player.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        cycles = cast.get_actors("cycles")
        cycle1 = cycles[0]
        cycle2 = cycles[1]

        if not self._is_game_over:
            cycle1.grow_trail(1)
            cycle2.grow_trail(1)

        head1 = cycle1.get_segments()[0]
        segments1 = cycle1.get_segments()[1:]
        score1, score2 = cast.get_actors("scores")

        head2 = cycle2.get_segments()[0]
        segments2 = cycle2.get_segments()[1:]
                
        for segment in segments1:
            points = cycle2.get_points()
            if head1.get_position().equals(segment.get_position()):
                score2.add_points(points)
                self._is_game_over = True
            for segment in segments2:
                if head1.get_position().equals(segment.get_position()):
                    score2.add_points(points)
                    self._is_game_over = True

        for segment in segments2:
            points2 = cycle2.get_points()
            if head2.get_position().equals(segment.get_position()):
                score1.add_points(points2)
                self._is_game_over = True
            for segment in segments1:
                if head2.get_position().equals(segment.get_position()):
                    score1.add_points(points)
                    self._is_game_over = True

    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the Cyclist and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycles = cast.get_actors("cycles")
            cycle1 = cycles[0]
            segments1 = cycle1.get_segments()

            cycle2 = cycles[1]
            segments2 = cycle2.get_segments()

            food = cast.get_first_actor("foods")

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments1:
                segment.set_color(constants.WHITE)
            for segment in segments2:
                segment.set_color(constants.WHITE)
            food.set_color(constants.WHITE)

    def get_is_game_over(self):
        return self._is_game_over