import random
import operator
from collections import defaultdict, OrderedDict


class Board():

  def __init__(self, n, row_size):
    self._n = n
    self._row_size = row_size

  @property
  def n(self):
    return self._n

  @classmethod
  def build_space(cls, players, size):
    """Build the space."""
    # sort
    players.sort()
    # build string, increment player ids (0 is player 1.)
    players = [str('%s' % (player + 1)) for player in players]
    ret = '[' + ','.join(players) + ']'
    return ret.ljust(size) # fill the rest with spaces

  def show(self, player_positions=None):
    """Print board tiles. Show player positions.

    player_positions: dict (position -> player id)
    """
    rows = []
    space_size = 20
    for i in xrange(0, self._n, self._row_size):
      row_num = i // self._row_size
      row = []
      if player_positions:
        # build row columns
        # alternating rows. First row start from left to right, second from right to left...
        if row_num % 2: # odd has reverse order
          for j in xrange(i + self._row_size - 1, i - 1, -1):
            space = ' ' * space_size
            if j < self.n: # ignore bigger numbers
              # player locations
              players = player_positions.get(j)
              if players:
                # show players
                space = self.build_space(players, space_size)

              row.append(str('%0.3d%s' % (j + 1, space)))
        else: # even has normal order
          for j in xrange(i, i + self._row_size):
            space = ' ' * space_size
            if j < self.n:
              # player locations
              players = player_positions.get(j)
              if players:
                # show players
                space = self.build_space(players, space_size)

              row.append(str('%0.3d%s' % (j + 1, space)))
      else:
        # no need to place player positions
        if row_num % 2: # odd has reverse order
          row = [str('%0.3d%s' % (j + 1, space)) for j in xrange(i + self._row_size - 1, i - 1, -1) if j < self._n]
        else: # even has normal order
          row = [str('%0.3d%s' % (j + 1, space)) for j in xrange(i, i + self._row_size) if j < self._n]
      if row:
        rows.append(row)

    rows.reverse()
    for row in rows:
        print(' | '.join(row))


class Game():

  def __init__(self, n, row_size, num_players=2, debug=False):
    self._board = Board(n, row_size)
    self._num_players = num_players
    self._winner = None
    # self._current_player = 0
    self._completed = False
    self.init_positions()
    self._debug = debug

  @property
  def n(self):
    """Number of boxes on the board."""
    return self._board.n

  @property
  def players(self):
    return self._players

  @property
  def is_completed(self):
    """Return public _completed

    return bool
    """
    return self._completed

  def set_completed(self, value=True):
    """Set value

    value: bool
    """
    self._completed = value

  def init_positions(self):
    """Initilize the player positions"""
    self._players = [] # list of dict
    for i in xrange(self._num_players):
      self._players.append({
        'position': 0
      })

  def roll_dice(self):
    """Generate random number."""
    return random.randint(1, 6)

  def auto_play(self):
    """Automated game"""
    current_player = 0
    while not self.is_completed:
      # roll the dice and play the round for the current player
      current_player = self.play_round(current_player, dice=self.roll_dice())
    if self._debug:
      print 'Winner : player %s' % (self._winner + 1)

  def play_round(self, player, dice):
    """Play round for a player"""
    position = self._players[player]['position'] + dice
    n = self.n - 1
    if self._debug:
      print 'Player : %s moved from %s to position: %s , dice: %s' % (player + 1, self._players[player]['position'] + 1, position + 1, dice)
    if position == n: # winner
      self.set_completed()
      self._winner = player
    elif position > n:
      position = self.n - (position - n)

    self._players[player]['position'] = position
    # move to next player
    return (player + 1) % self._num_players

  @property
  def player_positions(self):
    """Return dict of position -> player id."""
    # prepare dict (using list as default_factory.)
    positions = defaultdict(list)
    for player_id, player in enumerate(self.players):
      # append the player id in location.
      positions[player['position']].append(player_id)
    return positions

  def show_board(self):
    """Print the board with current player locations"""
    self._board.show(self.player_positions)


def game_stats(num_games=600):
  """Run game many times to see win stats."""
  # create a dict (using int as default_factory.)
  players = defaultdict(int)
  # run game 600 times to get statistics. So far I always get higher % winnings for the player1. Good to be the first!
  for i in xrange(num_games):
    # run game with 100 tiles, show 10 tiles in a row, for 10 players
    board = Game(100, 10, 10)
    # play the game
    board.auto_play()

    players[board._winner] += 1

  # sort players by number of wins in decreasing order and put in OrderedDict.
  sorted_players = OrderedDict(sorted(players.items(), key=operator.itemgetter(1), reverse=True))
  print '-' * 55
  print 'Result of %s games' % (num_games)
  print '-' * 55
  for player_id, win_count in sorted_players.iteritems():
    print 'Player %s: %s' % (player_id + 1, win_count)


def play_game(num_players=5):
  """Play one game and print the final player locations at the end."""
  board = Game(n=100, row_size=5, num_players=50, debug=True)
  # play the game
  board.auto_play()
  # show the current player locations on the board
  board.show_board()


play_game()
