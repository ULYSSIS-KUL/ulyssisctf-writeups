# bin-bin writeup

We get two files: `bin.bin` and `challenge.bin`. According to the prompt, the flag should be in one of these files. Following this clue, along with the knowledge that the files have a `.bin` extension, we try to extract some information from them. 

A simple way to start is to look at what is inside `bin.bin`, for this, we can use tools like `hexdump` or even `strings`. 

```
debber@fedora: strings bin.bin
FLG{76931fac9dab2b36c248b87d6ae33f9a62d7183a5d57}
FLG{89e4b2d6b441e2411dc709e111c7e1e7acb6f8cac0bb}
FLG{2fc4c8bc2ae3baaab9165cc458e199cb89f51b135f70}
FLG{91a5abb0874df3e8cb4543a5eb93b0441e9ca4c2b0fb}
FLG{3d30875cbf29abd5b1acf38984b35ae882809dd4cfe7}
FLG{abc5c61baa52e053b4c3643f204ef259d2e98042a948}
FLG{aac5e884cb3ec7db925643fd34fdd467e2cca406035c}
FLG{b2744cb90a63e51c9737903343947e02086541e4c48a}
FLG{99630aa9aece153843a4b190274ebc955f8592e30a22}
FLG{05a485846248987550aaf2094ec59e7931dc650c7451}
FLG{cc61c0cb2c46a1b3f2c349faff763c7f8d14ddff9463}
FLG{51744378d62c59285a8d7915614f5a2ac9e0d68aca62}
FLG{48a9227ab8f1930ee38ac7a9d239c9b026a481e49d53}
FLG{161f9a9513fe5271c32e9c21d156eb9f1bea57f6ae4f}
FLG{1b1de3b7fd9cee2d9cca7b4c242d26c31d000b7f90b7}
FLG{fe48a131c7debfbe58165266de56e1edf26939af07ec}
FLG{69ab1b17d8db62143f2228b51551c3d2c7de3f5072bd}
FLG{4d18c3aeb64cb9e8cba838667b6ed2b2fcab04abae86}
FLG{76e318b402a7d15b30d2d7ddb78650cc6af82bc3d7aa}
FLG{805b02dd9aa523b7374a1323ee6b516d1b81e5f709c2}
FLG{ff30a085bd174201732e8cfb5c3443e61a79c84814f5}
FLG{c790edaf1c3fa9b0a1dbc6dabc2b5ed267244c458752}
FLG{002b106d6381fad58a7e193657bde0fe029120f83793}
FLG{16891f828b8d24a049e5b86d855bcfed56765f9da1ac}
FLG{54caeaf9257abc67b451bc70b0e52817dd1b704a6b41}
FLG{8a83fd4a9ca4c89e1a6e779f8d9e9df18747591e5b31}
FLG{4c05763edcd59632423ca83f14d6f073d784db2b7001}
FLG{643a6760f9f0dd6ddd0a59e241dc1ed720287896286f}
FLG{5cc3addf6c1adf6ed35f477b0022981e5e1fbfe1bfb8}
FLG{e26b5ba93253275bf6a44b3fa1051cdfe3b3f5d2725a}
FLG{9a580fd5b04525b3182fcd2b3fda124aca3c901406a2}
FLG{b55cd8b95d48d13e379f1ccbcdfc39fee4acc5523aa0}
FLG{bdef57e63a1f81cbaba9f45caaed48d06bfb3d168360}
FLG{42bed57cac84761bfeb59a0c81304908bb781e4bbdf2}
FLG{30d2e977374b97bd0b6b7d38b736428826a0f2729be2}
FLG{290256dc304e875c9d4b3fb2125ae3d0cd3130d61149}
FLG{89517aca97daa2485181eb31c07d2c6a5bcc587e048a}
FLG{6d2beacd6fe206f225c708461b41fdb5ad087c5dc4fc}
FLG{aeec3a3437a42e51b065d6e4332f71b109d3317681ab}
FLG{0fcbf31c9f1c23ba46b4f983af9214d13ac3ddf6c03f}
FLG{3e9854c4d47741a5576812be0b5cb8bf647b930687ec}
```

Great news, we found a flag! Actually we found a lot of flags... How do we know which one is the right one? We could of course enter every flag into the prompt on the CTF website, but that would take to long. Maybe we can get a clue about which one is correct from the other file `challenge.bin`. Running `strings` on this one reveals that it is the program which the prompt was talking about! The following line from the strings output reveals that it is a C program which was mistakenly compiled with debug information

```
GNU C17 10.2.1 20210110 -mtune=generic -march=x86-64 -g -fasynchronous-unwind-tables
```

This means that the next step is to hand this over to a decompiler and look at what is happening. 

```
  fp_bin = fopen("bin.bin", "wb");
  for ( j = 0; j <= 19; ++j )
  {
    for ( i = 0; i <= 43; ++i )
    {
      v3 = rand();
      sprintf(&str[i], "%x", (unsigned int)(v3 % 16));
    }
    snprintf(buffer, 0x32uLL, "FLG{%s}", str);
    fwrite(buffer, 0x32uLL, 1uLL, fp_bin);
    fflush(fp_bin);
  }
  snprintf(buffer, 0x32uLL, "FLG{%s}", argv[1]);
  fwrite(buffer, 0x32uLL, 1uLL, fp_bin);
  for ( j_0 = 0; j_0 <= 19; ++j_0 )
  {
    for ( i_0 = 0; i_0 <= 43; ++i_0 )
    {
      v4 = rand();
      sprintf(&str[i_0], "%x", (unsigned int)(v4 % 16));
    }
    snprintf(buffer, 0x32uLL, "FLG{%s}", str);
    fwrite(buffer, 0x32uLL, 1uLL, fp_bin);
    fflush(fp_bin);
  }
  fclose(fp_bin);
```

We can see that this is actually quite simple, the program just opens `bin.bin` in binary mode, and then inserts a few random flags. After that, it writes a flag that has been defined in the arguments when starting the program. Finally, it writes another few random flags. This means we just have to pick out the one flag which is not random! In this case, wee see that the first 19 flags are bogus, so we know number 20 should be the right one.
