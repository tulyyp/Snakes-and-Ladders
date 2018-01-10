import random


class Board():

  def __init__(self, n, row_size):
    self._n = n
    self._row_size = row_size

  @property
  def n(self):
    return self._n

  def show(self):
    rows = []
    for i in xrange(0, self._n, self._row_size):
      row_num = i // self._row_size
      row = None
      if row_num % 2: # odd has reverse order
        row = [str('%0.3d' % (j + 1)) for j in xrange(i + self._row_size - 1, i - 1, -1) if j < self._n]
      else: # even has normal order
        row = [str('%0.3d' % (j + 1)) for j in xrange(i, i + self._row_size) if j < self._n]
      if row:
        rows.append(row)

    rows.reverse()
    for row in rows:
        print(' | '.join(row))


class Game():

  def __init__(self, n, row_size, num_players=2):
    self._board = Board(n, row_size)
    self._num_players = num_players
    self._winner = None
    # self._current_player = 0
    self._completed = False
    self.init_positions()
    self._debug = False

  @property
  def n(self):
    """Number of boxes on the board."""
    return self._board.n

  def init_positions(self):
    self._players = []
    for i in xrange(self._num_players):
      self._players.append({
        'position': 0
      })

  def roll_dice(self):
    return random.randint(1, 6)

  def play(self):
    """Play Game"""
    current_player = 0
    while not self._completed:
      current_player = self.play_round(current_player)
    if self._debug:
      print 'Winner : player %s' % (self._winner + 1)

  def play_round(self, player):
    """Play round for a player"""
    dice = self.roll_dice()
    position = self._players[player]['position'] + dice
    n = self.n - 1
    if self._debug:
      print 'Player : %s moved from %s to position: %s , dice: %s' % (player + 1, self._players[player]['position'] + 1, position + 1, dice)
    if position == n: # winner
      self._completed = True
      self._winner = player
    elif position > n:
      position = self.n - (position - n)

    self._players[player]['position'] = position
    # move to next player
    return (player + 1) % self._num_players


def game_stats(num_games=600):
  """Run game many times to see win stats."""
  import operator
  from collections import defaultdict, OrderedDict
  # create a dict (using int as default_factory.)
  players = defaultdict(int)
  # run game 600 times to get statistics. So far I always get higher % winnings for the player1. Good to be the first!
  for i in xrange(num_games):
    # run game with 100 tiles, show 10 tiles in a row, for 10 players
    board = Game(100, 10, 10)
    # play the game
    board.play()

    players[board._winner] += 1
  # sort players by number of wins in decreasing order and put in OrderedDict.
  sorted_players = OrderedDict(sorted(players.items(), key=operator.itemgetter(1), reverse=True))
  print '-' * 55
  print 'Result of %s games' % (num_games)
  print '-' * 55
  for player_id, win_count in sorted_players.iteritems():
    print 'Player %s: %s' % (player_id + 1, win_count)


game_stats()
