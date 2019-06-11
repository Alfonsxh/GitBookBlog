# RAID

**独立硬盘冗余阵列(RAID, Redundant Array of Independent Disks)**，利用虚拟化技术将多个磁盘组合起来，成为一个多个硬盘的阵列，从而提升效率或者资料冗余。

根据RAID的层级不同，资料会以多种形式放置在多个磁盘上。

## RAID层级

RAID的层级，常用的包括：RAID0、RAID1、RAID5、RAID10。

### RAID 0 (stripe)



### RAID 1 (mirror)

### RAID 5 ()

### RAID 10 ()

## RAID信息查看

```bash
List of commands:

Commands   Description
-------------------------------------------------------------------
add        Adds/creates a new element to controller like VD,Spare..etc
delete     Deletes an element like VD,Spare
show       Displays information about an element
set        Set a particular value to a property 
start      Start background operation
stop       Stop background operation
pause      Pause background operation
resume     Resume background operation
download   Downloads file to given device
expand     expands size of given drive
insert     inserts new drive for missing
transform  downgrades the controller
/cx        Controller specific commands
/ex        Enclosure specific commands
/sx        Slot/PD specific commands
/vx        Virtual drive specific commands
/dx        Disk group specific commands
/fx        Foreign configuration specific commands
/px        Phy specific commands
/bbu       Battery Backup Unit related commands
```

## 参考

- [Advantages and disadvantages of various RAID levels](https://datapacket.com/blog/advantages-disadvantages-various-raid-levels/)
- [What is RAID 0, 1, 5, & 10?](https://www.youtube.com/watch?v=U-OCdTeZLac)
- [RAID 磁盘阵列配置和调优小结](https://wsgzao.github.io/post/raid/)
