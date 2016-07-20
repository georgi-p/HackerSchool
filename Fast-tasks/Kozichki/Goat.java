import java.util.Arrays;
import java.io.*;

class Goat {

	private int N;
	private int K;
	private int[] goats;
	private int[] sorted;
	private int capacity;
	private int max;

	Goat(int N, int K, int[] goats, int max){
		this.N = N;
		this.K = K;
		this.max = max;
		this.goats = goats;
		this.sorted = goats;
		Arrays.sort(sorted);
		this.capacity = max;
		findCapacity();
	}

	private void findCapacity(){
		Boolean flag = false;

		int left = max; int right = N*max;

		while(left < right){
			capacity = (left + right) / 2;
			flag = runCurrentConfiguration();
			if(flag){ right = capacity; }
			else{ left = capacity + 1; }
		}
		capacity = (left + right) / 2;
	}

	Boolean runCurrentConfiguration(){

		// goatsbycount[i] is the number of goats that weigh i
		int[] goatsbycount = new int[max+1];
		for(int i = 0; i < N; i++){
			goatsbycount[goats[i]] += 1;
		}

		// The current load of the boat
		int currentload;
		int k = 0;
		// Number of goats that have not crossed the river yet
		int numberofgoats = N;

		// We have k rounds
		while(k < K){
			currentload = 0;
			for(int i = N-1; i >= 0; i--){
				// If we can put this goat without exceeding the capacity and this goat has not yet crossed
				if(currentload + sorted[i] <= capacity && goatsbycount[sorted[i]] > 0){
					currentload += sorted[i];
					goatsbycount[sorted[i]] -= 1;
					numberofgoats -= 1;
				}
			}
			k += 1;
		}

		// If all goats have crossed then this capacity works
		return numberofgoats == 0;
	}

	public int getCapacity(){
		return capacity;
	}

	public String toString(){ 
		String str = "Shepherd with N = " + N + ", K = " + K + ", and goat weights ";
		for(int i = 0; i < N; i++){
			str += goats[i];
			if(i != N-1){ str += ", "; }
		}
		return str += ".";
	}

	public static void main(String[] args) throws IOException{
		
/*		BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
		String line;
		while ((line = stdin.readLine()) != null && line.length()!= 0) {
    			String[] input = line.split(" ");
			System.out.println(input);
  		  }
*/




		// Get keyboard input
		// The number of arguments should be at least 2 - number of goats and number of iterations
		assert(args.length >= 2);

		int N = Integer.parseInt(args[0]);
		assert(1 <= N && N <= 1000);

		int K = Integer.parseInt(args[1]);
		assert(1 <= K && K <= 1000);

		// The number of arguments should be exactly 2 + the number of goats
		assert(args.length == 2+N);
		int[] goats = new int[N];

		int max = 0;

		// Fill up the array with goat weights and update the max weight
		for(int i = 0; i < N; i++){
			goats[i] = Integer.parseInt(args[i+2]);
		//	assert(1 <= goats[i] && goats[i] <= 100000);
			if(max < goats[i]){ max = goats[i]; }
		}

		Goat g = new Goat(N, K, goats, max);

		System.out.println("The least capacity is: " + g.getCapacity());
//		System.out.println(g.runCurrentConfiguration());

	}
}
