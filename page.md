# **Title** : **Visualizing Mathematical Analysis of Stock data**

# **Objectives**:
- #### Gather real time data about the stock market
- #### Process the data to generate information on the prediction of the stock
- #### Visualize the same data in different graphs

# **Presented By:**
- #### Tarun Gopalkrishna A
- #### Semester 5(3rd Year)

# **Abstract:**
```
root
    \
     back_end
     |       \
     |        input.py (socket hosted as the server)
     |        database.py (module to handle ORM and connection to the database)
     |        analytics.py (module to calculate analytics about the gathered data)
     |        UserDefinedFunctions.py (user defined functions written by the developer/User)
     |        mysqlConnector.py (layer above the database to handle all CRUD operations)
     |        .config
     |               \
     |                database.json (definition of the database)
     |                mysql.cnf (credentials to connect to the database)
     front_end
              \
               App.js
               index.js
               Components
                         \
                          Landing.js (opening page)
                          Users.js (page with respect to users subscription)
```

# **Requirements:**
#### Front End : React JS
#### Server    : Python3
#### Back End  : Python3
#### Database  : mySQL
#### OS        : Ubuntu 18.04
#### Processor :
```
			Architecture:        x86_64
			CPU op-mode(s):      32-bit, 64-bit
			Byte Order:          Little Endian
			CPU(s):              4
			On-line CPU(s) list: 0-3
			Thread(s) per core:  2
			Core(s) per socket:  2
			Socket(s):           1
			NUMA node(s):        1
			Vendor ID:           GenuineIntel
			CPU family:          6
			Model:               42
			Model name:          Intel(R) Core(TM) i3-2310M CPU @ 2.10GHz
			Stepping:            7
			CPU MHz:             855.141
			CPU max MHz:         2100.0000
			CPU min MHz:         800.0000
			BogoMIPS:            4190.64
			Virtualization:      VT-x
			L1d cache:           32K
			L1i cache:           32K
			L2 cache:            256K
			L3 cache:            3072K
			NUMA node0 CPU(s):   0-3
			Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx
                                 fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good
                                 nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2
                                 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer xsave avx lahf_lm
                                 epb pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid xsaveopt dtherm arat
                                 pln pts md_clear flush_l1d
```
### Ram       : 3.8 GB

# **Entities:**
<pre>
+------------+--------------------------------------------------------------------+
| TABLE NAME |                              ENTITIES                              |
+------------+--------------------------------------------------------------------+
|   Users    |id,user_name,phone,email,subscription_type,amount_payed             |
+------------+--------------------------------------------------------------------+
|   VWAP     |volume,closing_price,total_traded_value,sigma_1,sigma_2,z_value,vwap|
+------------+--------------------------------------------------------------------+
|    RSI     |avg_14_up,avg_14_down,rsi                                           |
+------------+--------------------------------------------------------------------+
| Stochastic |high,low,close,percent_k,percentage_d                               |
+------------+--------------------------------------------------------------------+
|  Acc/Dist  |close,open,high,low,a/d                                             |
+------------+--------------------------------------------------------------------+
|    MACD    |ema_12,ema_26,signal,volume,macd,macd_hist                          |
+------------+--------------------------------------------------------------------+
|bolingerBand|ema_21,sigma_1,sigma_1.5,sigma_2,sigma_2.5,sigma_3,asqd             |
+------------+--------------------------------------------------------------------+
</pre>
