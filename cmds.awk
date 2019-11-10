BEGIN {
    dir=command_dir "/" device
    print "Creating commands in " dir
    system("mkdir -p " dir)
}

{
    system("echo " $2 ">" dir "/" $1)
}
