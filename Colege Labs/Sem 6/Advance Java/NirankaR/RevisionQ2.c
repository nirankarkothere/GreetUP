#include<stdio.h>
int main(){
	int a[10][10],r,c,i,j;
	
	printf("Enter the number of row and column :");
	scanf("%d%d",&r,&c);

	printf("Enter the number of matrics : \n");

	for(i=0;i<r;i++){
		for(j=0;j<c;j++){
		scanf("%d",&a[i][j]);
		}
	}

	printf("element of 2d array are :\n");

	for(i=0;i<r;i++){
		for(j=0;j<c;j++){
			printf("%d \t ",a[i][j]);
		}

		printf("\n");
	}

	return 0;
}

