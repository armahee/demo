public class q1 {
    public static void it(int[][] m){
        int[] arr = new int[m.length];
        for(int i=0;i<m.length;i++){
            arr[i]=0;
            for(int j=1;j<m[0].length;j++){
                if(m[i][j]>m[i][arr[i]]){
                    arr[i]=j;
                }
            }
        }
        for(int j=0;j<m[0].length;j++){
            int mn=0;
            for(int i=0;i<m.length;i++){
                if(m[i][j]<m[mn][j]){
                    mn=i;
                }
            }
            if(arr[mn]==j){
                System.out.printf("Treasure found at(%d,%d) with value: %d\n",mn,j,m[mn][j]);
                return;
            }
        }
        System.out.printf("No treasure found.\n");
        return;
    }
    public static void main(String[] args){
        int[][] m={{8,10,9},{7,5,6},{3,4,2},{10,12,11}};
        it(m);
    }
}
