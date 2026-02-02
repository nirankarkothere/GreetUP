#include<stdio.h>
int main(){
	int a[10][10],r,p,i,j;
	printf("Enter the number of rows and column :");
	scanf("%d%d",&r,&p);

	printf("Enter the number of matrics :\n ");

	for(i=0;i<r;i++){
		for(j=0;j<p;j++){
		scanf("%d",&a[i][j]);
		}
	}

	printf("elements 1st 2d array are :\n");
	for(i=0;i<r;i++){
		for(j=0;j<p;j++){
                printf("%d\t",a[i][j]);
                }
		printf("\n");
        }

	

	return 0;

}


