#include<stdio.h>
#include<stdlib.h>
#include<time.h>
void merge(int arr[],int s,int m,int e);
void divide(int arr[],int s,int e);
 void divide(int arr[],int s,int e){
     if(s<e){
               int mid = s+(e-s)/2;
               divide(arr,s,mid);
               divide(arr,mid+1,e);
               merge(arr,s,mid,e);
               
     } 
     
 }
 void merge(int arr[],int s,int mid,int e){
     int temp[10000];
     int k=s;
     int i=s;
     int j=mid+1;
     while(i<=mid&&j<=e){
         if(arr[i]<arr[j]){
             temp[k++]=arr[i];
             i++;
         }
         else{
             temp[k++]=arr[j];
             j++;
         }
     }
     
     while(i<=mid){
         temp[k++]=arr[i++];

     }
     
     while(j<=e){
         temp[k++]=arr[j++];

     }
     
    for(k =s;k<=e;k++)
        arr[k]=temp[k];
 }
 
 int main(){
     int arr[1000],n;
     clock_t start, end;
     
      printf("Enter number of customer IDs: ");
    scanf("%d", &n);
     printf("Randomly generated customer IDs:\n");
     
      for(int i=0;i<n;i++){
          arr[i]=rand()%100;
          printf("%d ",arr[i]);
      }
      
      start=clock();
      divide(arr,0,n-1);
       end = clock();
       
           printf("\nSorted Customer IDs:\n");

    for(int i = 0; i < n; i++)
        printf("%d ", arr[i]);

    double time = (double)(end - start) / CLOCKS_PER_SEC;

    printf("\nMerge Sort Execution Time = %lf seconds", time);

    return 0;

      
 }
 
 
 
 
 
 
 
 
 
 
 
 
 


