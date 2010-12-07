#include <stdio.h>

int main()
{
 int c ;
 setlinebuf(stdout);
  for(;;)
  {
   c = getchar() ;
   printf("%c = %d\n", c, c) ;
  }
 return 0 ;
}
