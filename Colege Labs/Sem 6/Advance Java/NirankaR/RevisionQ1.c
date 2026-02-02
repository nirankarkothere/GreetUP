#include<stdio.h>
int main(){
	int a[10],n,i;

	printf("Enter the nimber of elements : ");
	scanf("%d",&n);

	printf("Enter %d elements : \n ",n);

	for(i=0;i<n;i++){
		scanf("%d",&a[i]);
	}

	printf("The elements of array are \n ");

        for(i=0;i<n;i++){
                printf("%d",a[i]);
        }

	return 0;
}
