package myTests;

import java.util.Scanner;
import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors
import java.lang.Math;
import java.util.*;

public class Main {
	public static byte performIterativeSearch(State currentState, String pathName) {

		// safty first write
		try {
			FileWriter myWriter = new FileWriter(pathName);
			myWriter.write(String.valueOf(1));
			myWriter.close();
		    }
		catch (IOException e) {
			e.printStackTrace();
		}
		byte currentdepth = 4; // Starting depth, depth 4 should be easy with b = 12 as 12^4 = 20.736
		byte bestMove = 0;
		long startTime = System.currentTimeMillis();
		byte newMove = -1;
		
		while (System.currentTimeMillis() - startTime < 800) {
			newMove = makeMove(currentState, currentdepth);
			
	    	if(newMove != (byte)-1) {
	    		bestMove = newMove; // safety first write should be here
	    	}
	    	else {
	    		return bestMove;
	    	}
	    	
			try {
				FileWriter myWriter = new FileWriter(pathName);
				if(bestMove != 11) {
					myWriter.write(String.valueOf(bestMove + 1));
				}
				else {
					myWriter.write("flip");
				}
				myWriter.close();
  		    }
			catch (IOException e) {
				e.printStackTrace();
			}
        	currentdepth++;
	    }
	    return bestMove;
	}
		
    public static byte makeMove(State currentState, byte depth) {
    	byte[] moveEvalOrder = {(byte)5,(byte)6,(byte)4,(byte)7,(byte)3,(byte)8,(byte)2,(byte)9,(byte)1,(byte)10,(byte)0,(byte)11};
        byte bestMove = 0;
        byte currentMove;
        short bestScore;
        if(currentState.whiteToMove) {
        	bestScore = Short.MIN_VALUE;
        }
        else {
        	bestScore = Short.MAX_VALUE;
        }
        
        boolean[] possibleMoves = currentState.getPossibleMoves();
        for (byte column = 0; column < possibleMoves.length; column++) {
        	currentMove = moveEvalOrder[(int)column];
            if (possibleMoves[currentMove]) {
                State nextState = new State(currentState, currentMove);
                short score = minimax(nextState, depth, Short.MIN_VALUE, Short.MAX_VALUE, !currentState.whiteToMove);
                
                if (score > bestScore && currentState.whiteToMove) {
                    bestScore = score;
                    bestMove = currentMove;
                }
                else if(score < bestScore && !currentState.whiteToMove){
                    bestScore = score;
                    bestMove = currentMove;
                }
            }
        }
        return bestMove;
    }
    
    private static short minimax(State state, int depth, short alpha, short beta, boolean maximizingPlayer) {
    	if(depth == 0) {
    		return state.evaluation;
    	}
        if (state.GameOver()) { 
        	if(state.evaluation == Short.MAX_VALUE || state.evaluation == Short.MIN_VALUE) {
            	return state.evaluation;
        	}
        	return (short)0;
        }
        
        boolean[] possibleMoves = state.getPossibleMoves();
        
        if (maximizingPlayer) {
            short maxEval = Short.MIN_VALUE;
            
            for (byte column = 0; column < possibleMoves.length; column++) {
                if (possibleMoves[column]) {
                    State nextState = new State(state, column);
                    short eval = minimax(nextState, depth - 1, alpha, beta, false);
                    if(eval == Short.MAX_VALUE) {
                    	return Short.MAX_VALUE;
                    }
                    maxEval = (short)Math.max(maxEval, eval);
                    alpha = (short)Math.max(alpha, eval);
                    
                    if (beta <= alpha) {
                        break;
                    }
                }
            }
            return maxEval;
        } 
        short minEval = Short.MAX_VALUE;
        for (byte column = 0; column < possibleMoves.length; column++) {
        	if (possibleMoves[column]) {
        		State nextState = new State(state, column);
        		short eval = minimax(nextState, depth - 1, alpha, beta, true);
        		if(eval == Short.MIN_VALUE) {
        			return Short.MIN_VALUE;
        		}
        		minEval = (short)Math.min(minEval, eval);
        		beta = (short)Math.min(beta, eval);
        		
        		if (beta <= alpha) {
        			break;
        		}
        	}
        }
        return minEval;
    }
    
    public static void main(String[] args) {
    	if(args.length == 2) {
    		Boolean[][] board = new Boolean[11][8];
    		int movesPlayed = 0;
    		boolean NowlastMoveFlipped = false;
    		int countWhite = 0; // to eval if white can flip
    		boolean NowwhiteCanFlip = true;
    		int countBlack = 0; // to eval if black can flip
    		boolean NowblackCanFlip = true;
    		boolean whiteToPlay = false;
    		
        	try {
                File file = new File(args[0]);
                Scanner scanner = new Scanner(file);
                
                movesPlayed = Integer.parseInt(scanner.nextLine().split(" ")[1]);   
                if(scanner.nextLine().split(" ")[2].equalsIgnoreCase("flip")) {
                	NowlastMoveFlipped = true;
                }
                while (scanner.hasNextLine()) {
                    String line = scanner.nextLine();
                    if (line.equals("Current-State:")) {
                        break;
                    }
                }
                
                // Spielfeld einlesen und in Boolean-Array konvertieren
                for (int row = 7; row >= 0; row--) {
                    String line = scanner.nextLine();
                    for (int col = 0; col < 11; col++) {
                        char cell = line.charAt(col);
                        if (cell == 'e') {
                            board[col][row] = null;
                        } else if (cell == 'A') {
                            board[col][row] = true;
                            countWhite++;
                        } else if (cell == 'B') {
                            board[col][row] = false;
                            countBlack++;
                        }
                    }
                }
                
                scanner.close();
                
                
            } catch (FileNotFoundException e) {
            	System.out.println("An error occured");
                e.printStackTrace();
            }
        	if(Math.floor((movesPlayed + 1)/2) != countWhite) {
        		NowwhiteCanFlip = false;
        	}
        	if(Math.ceil((movesPlayed - 1.0)/2.0)  != countBlack) {
        		NowblackCanFlip = false;
        	}
        	if(movesPlayed % 2 == 0) {
        		whiteToPlay = true;
        	}
        	State currentState = new State(board, whiteToPlay, NowwhiteCanFlip, NowblackCanFlip, NowlastMoveFlipped);
        	performIterativeSearch(currentState, args[1]);
    	}
    	else {
    		System.out.println("Wrong Call! We only have number of arguments: " + args.length);
    		for (int i = 0; i< args.length;i++) {
    			System.out.println("We have argument number: " + i + " which includes: " + args[i]);
    		}
    	}
    }
}

public class State {
	/* To simplify things: White plays against black (like in chess)
	 * White represents true values of the board, black is false and null is not occupied
	 */
	public State parent;
	public Boolean[][] board; // List of columns
	public short evaluation; // evaluation of the current state.  Connected 1 has evaluation +-1
	
	public boolean whiteToMove; // obviously true when white has to Move
	public boolean whiteCanFlip; // obviously true when white can flip
	public boolean blackCanFlip; // obviously true when black can flip
	public boolean lastMoveFlipped; // signalizes if the last move was a flip
	
	public State(State parent, Boolean[][] board) {
		this.parent = parent;
		this.board = board;
		
		if(parent == null) {
			evaluation = 0;
			whiteCanFlip = true;
			blackCanFlip = true;
			whiteToMove = true;
		}
		else {
			whiteToMove = !parent.whiteToMove; // now the other person has to make a move
		}
	}
	
	public State(State parent, byte column) {
		// calls the constructor with the parent and the copied board (source from stack overflow)
		// https://stackoverflow.com/questions/5617016/how-do-i-copy-a-2-dimensional-array-in-java
		// called last at 15.06
		this(parent, Arrays.stream(parent.board).map(Boolean[]::clone).toArray(Boolean[][]::new)); 

		this.whiteCanFlip = parent.whiteCanFlip;
		this.blackCanFlip = parent.blackCanFlip;
		
		// if the move was to flip the board then change the status of white/black-CanFlip
		if(column == 11) {
			if(whiteToMove) {
				blackCanFlip = false;
			}
			else {
				whiteCanFlip = false;
			}
			flipBoard();
			lastMoveFlipped = true;
		}
		else {
			lastMoveFlipped = false;
			addCoin(column);
		}
		evaluatePosition();
	}
	
	public State(Boolean[][] board, boolean whiteToMove, boolean whiteCanFlip, boolean blackCanFlip, boolean lastMoveFlipped) {
		this.board = board;
		this.parent = null;
		this.whiteToMove = whiteToMove;
		this.whiteCanFlip = whiteCanFlip;
		this.blackCanFlip = blackCanFlip;
		this.lastMoveFlipped = lastMoveFlipped;
		evaluatePosition();
	}
	
	public void flipBoard() {
		Boolean[][] newBoard = new Boolean[11][8];
		byte k;
		for (byte i = 0; i < 11; i++) {
			k = 0;
			for (byte j = 7; j >= 0; j--) {
				if(board[i][j] != null) {
					newBoard[i][k] = board[i][j];
					k++;
				}
			}
		}
		board = newBoard;
	}
	
	public byte addCoin(byte column) { // returns the row where the coin is inserted.
		for (byte i = 0; i < 8; i++) {
			if(board[column][i] == null) {
				board[column][i] = !whiteToMove; // we have to inverse it, because if it is whiteToveMove, then the last move was from the opponent.
				return i;
			}
		}
		return (byte)-1; //error
	}
	
	public boolean[] getPossibleMoves() {
		boolean[] freeColumn = new boolean[12]; // the 12th column represents the possibility to flip initially all false
		if(evaluation == Short.MAX_VALUE || evaluation == Short.MIN_VALUE) { //then the game is over
			return freeColumn;
		}
		for (byte i = 0; i < 11; i++) {
			if(board[i][7] == null) {
				freeColumn[i] = true;
			}
		}
		// check the conditions to flip the board
		freeColumn[11] = (whiteToMove && whiteCanFlip && !lastMoveFlipped) || (!whiteToMove && blackCanFlip && !lastMoveFlipped);
		return freeColumn;
	}
	
	public void evaluatePosition() {
		
		short eval = (short)0;
		byte nullCounter = (byte)0;
		byte whiteCounter = (byte)0;
		byte blackCounter = (byte)0;
		boolean lostOne = false;
		
		// This evaluates a position out of nothing.
		// check columnwise 
		for(byte column = 0;column<11;column++) {
			for(byte row = 0;row<8;row++) {
				if(board[column][row] == null) {
					nullCounter++;
				}
				else if(board[column][row]) {
					whiteCounter++;
					if(blackCounter > 0) {
						blackCounter = (byte)0;
						nullCounter = 0;
					}
				}
				else {
					blackCounter++;
					if(whiteCounter > 0) {
						whiteCounter = (byte)0;
						nullCounter = 0;
					}
				}
				if(nullCounter + whiteCounter == 5 && whiteCounter >= 1 && !lostOne) {
					if(whiteCounter == 5) {
						this.evaluation = Short.MAX_VALUE;
						return;
					}
					eval = (short)(eval + Math.pow(2,  whiteCounter - 1));
				}
				else if(nullCounter + blackCounter == 5 && blackCounter >= 1 && !lostOne) {
					if(blackCounter == 5) {
						this.evaluation = Short.MIN_VALUE;
						return;
					}
					eval = (short)(eval - Math.pow(2,  blackCounter - 1));
				}
				if(nullCounter + whiteCounter + blackCounter >= 5) {
					if(board[column][row-4] == null) {
						nullCounter--;
						lostOne = false;
					}
					else if(board[column][row-4]) {
						whiteCounter--;
						lostOne = true;
					}
					else {
						blackCounter--;
						lostOne = true;
					}
				}
			}
			lostOne = false;
			whiteCounter = blackCounter = nullCounter = (byte)0;
		}
		
		// check horizontally
		for(byte row = 0;row<8;row++) {
			for(byte column = 0;column<11;column++) {
				if(board[column][row] == null) {
					nullCounter++;
				}
				else if(board[column][row]) {
					whiteCounter++;
					if(blackCounter > 0) {
						blackCounter = (byte)0;
						nullCounter = 0;
					}
				}
				else {
					blackCounter++;
					if(whiteCounter > 0) {
						whiteCounter = (byte)0;
						nullCounter = 0;
					}
				}
				if(nullCounter + whiteCounter == 5 && whiteCounter >= 1 && !lostOne) {
					if(whiteCounter == 5) {
						this.evaluation = Short.MAX_VALUE;
						return;
					}
					eval = (short)(eval + Math.pow(2, whiteCounter - 1));
				}
				else if(nullCounter + blackCounter == 5 && blackCounter >= 1 && !lostOne) {
					if(blackCounter == 5) {
						this.evaluation = Short.MIN_VALUE;
						return;
					}
					eval = (short)(eval - Math.pow(2, blackCounter - 1));
				}
				if(nullCounter + whiteCounter + blackCounter >= 5) {
					if(board[column-4][row] == null) {
						nullCounter--;
						lostOne = false;
					}
					else if(board[column-4][row]) {
						whiteCounter--;
						lostOne = true;
					}
					else {
						blackCounter--;
						lostOne = true;
					}
				}
			}
			lostOne = false;
			whiteCounter = blackCounter = nullCounter = (byte)0;
		}
		
		// check this diagonal \
		for (byte k = 4; k<8+11-4;k++) {
			byte row = (byte)Math.min(k, 7);
			byte column = (byte)Math.max(0, k-7);
			for (byte i = 0; i<Math.min(10-column, row)+1;i++) {
				if(board[column + i][row - i] == null) {
					nullCounter++;
				}
				else if(board[column+i][row-i]) {
					whiteCounter++;
					if(blackCounter > 0) {
						blackCounter = (byte)0;
						nullCounter = 0;
					}
				}
				else {
					blackCounter++;
					if(whiteCounter > 0) {
						whiteCounter = (byte)0;
						nullCounter = 0;
					}
				}
				if(nullCounter + whiteCounter == 5 && whiteCounter >= 1 && !lostOne) {
					if(whiteCounter == 5) {
						this.evaluation = Short.MAX_VALUE;
						return;
					}
					eval = (short)(eval + Math.pow(2,  whiteCounter - 1));
				}
				else if(nullCounter + blackCounter == 5 && blackCounter >= 1 && !lostOne) {
					if(blackCounter == 5) {
						this.evaluation = Short.MIN_VALUE;
						return;
					}
					eval = (short)(eval - Math.pow(2,  blackCounter - 1));
				}
				if(nullCounter + whiteCounter + blackCounter >= 5) {
					if(board[column+i-4][row-i+4] == null) {
						nullCounter--;
						lostOne = false;
					}
					else if(board[column+i-4][row-i+4]) {
						whiteCounter--;
						lostOne = true;
					}
					else {
						blackCounter--;
						lostOne = true;
					}
				}
			}
			lostOne = false;
			whiteCounter = blackCounter = nullCounter = (byte)0;
		}
		
		// check this diagonal / 
		for (byte k = 3; k>-7;k--) { //-7 = 8 - 11 - 4
			byte column = (byte)Math.max(0, -k);
			byte row = (byte)Math.max(0, k);
			for (byte i = row; i<Math.min(8-row, 11-column);i++) {
				if(board[column + i][row + i] == null) {
					nullCounter++;
				}
				else if(board[column+i][row+i]) {
					whiteCounter++;
					if(blackCounter > 0) {
						blackCounter = (byte)0;
						nullCounter = 0;
					}
				}
				else {
					blackCounter++;
					if(whiteCounter > 0) {
						whiteCounter = (byte)0;
						nullCounter = 0;
					}
				}
				if(nullCounter + whiteCounter == 5 && whiteCounter >= 1 && !lostOne) {
					if(whiteCounter == 5) {
						this.evaluation = Short.MAX_VALUE;
						return;
					}
					eval = (short)(eval + Math.pow(2,  whiteCounter - 1));
				}
				else if(nullCounter + blackCounter == 5 && blackCounter >= 1 && !lostOne) {
					if(blackCounter == 5) {
						this.evaluation = Short.MIN_VALUE;
						return;
					}
					eval = (short)(eval - Math.pow(2,  blackCounter - 1));
				}
				if(nullCounter + whiteCounter + blackCounter >= 5) {
					if(board[column+i-4][row+i-4] == null) {
						nullCounter--;
						lostOne = false;
					}
					else if(board[column+i-4][row+i-4]) {
						whiteCounter--;
						lostOne = true;
					}
					else {
						blackCounter--;
						lostOne = true;
					}
				}
			}
			lostOne = false;
			whiteCounter = blackCounter = nullCounter = (byte)0;
		}
		this.evaluation = eval;
	}

	public boolean GameOver() {
		if(this.evaluation == Short.MAX_VALUE || this.evaluation == Short.MIN_VALUE) {
			return true;
		}
		boolean[] moves = getPossibleMoves();
		for(byte i = 0;i<11;i++) {
			if(moves[i]) {
				return false;
			}
		}
		return true;
	}
}