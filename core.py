import random


class Node:
    def __init__(self):
        self.keys = []
        self.children = []

    @property
    def leaf(self):
        return len(self.children) == 0


class BTree:
    def __init__(self, t):
        """
        Initializing the B-Tree
        """
        self.root = Node()
        self.t = t

    def printTree(self, x, lvl=0):
        """
        Prints the complete B-Tree
        :param x: Root node.
        :param lvl: Current level.
        """
        print("Level ", lvl, " --> ", len(x.keys), end=": ")
        for i in x.keys:
            print(i, end=" ")
        print()
        lvl += 1
        if len(x.children) > 0:
            for i in x.children:
                self.printTree(i, lvl)

    def search(self, k, x=None):
        """
        Search for key 'k' at position 'x'
        :param k: The key to search for.
        :param x: The position to search from. If not specified, then search occurs from the root.
        :return: 'None' if 'k' is not found. Otherwise returns a tuple of (node, index) at which the key was found.
        """
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i][0]:
                i += 1
            if i < len(x.keys) and k == x.keys[i][0]:
                return x, i
            elif x.leaf:
                return None
            else:
                # Search its children
                return self.search(k, x.children[i])
        else:
            # Search the entire tree
            return self.search(k, self.root)

    def insert(self, k):
        """
        Calls the respective helper functions for insertion into B-Tree
        :param k: The key to be inserted.
        """
        root = self.root
        # If a node is full, split the child
        if len(root.keys) == (2 * self.t) - 1:
            temp = Node()
            self.root = temp
            # Former root becomes 0'th child of new root 'temp'
            temp.children.insert(0, root)
            self._splitChild(temp, 0)
            self._insertNonFull(temp, k)
        else:
            self._insertNonFull(root, k)

    def _insertNonFull(self, x, k):
        """
        Inserts a key in a non-full node
        :param x: The key to be inserted.
        :param k: The position of node.
        """
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._splitChild(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            self._insertNonFull(x.children[i], k)

    def _splitChild(self, x, i):
        """
        Splits the child of node at 'x' from index 'i'
        :param x: Parent node of the node to be split.
        :param i: Index value of the child.
        """
        t = self.t
        y = x.children[i]
        z = Node()
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]

    def delete(self, x, k):
        """
        Calls the respective helper functions for deletion from B-Tree
        :param x: The node, according to whose relative position, helper functions are called.
        :param k: The key to be deleted.
        """
        t = self.t
        i = 0
        while i < len(x.keys) and k[0] > x.keys[i][0]:
            i += 1
        # Deleting the key if the node is a leaf
        if x.leaf:
            if i < len(x.keys) and x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return

        # Calling '_deleteInternalNode' when x is an internal node and contains the key 'k'
        if i < len(x.keys) and x.keys[i][0] == k[0]:
            return self._deleteInternalNode(x, k, i)
        # Recursively calling 'delete' on x's children
        elif len(x.children[i].keys) >= t:
            self.delete(x.children[i], k)
        # Ensuring that a child always has atleast 't' keys
        else:
            if i != 0 and i + 2 < len(x.children):
                if len(x.children[i - 1].keys) >= t:
                    self._deleteSibling(x, i, i - 1)
                elif len(x.children[i + 1].keys) >= t:
                    self._deleteSibling(x, i, i + 1)
                else:
                    self._deleteMerge(x, i, i + 1)
            elif i == 0:
                if len(x.children[i + 1].keys) >= t:
                    self._deleteSibling(x, i, i + 1)
                else:
                    self._deleteMerge(x, i, i + 1)
            elif i + 1 == len(x.children):
                if len(x.children[i - 1].keys) >= t:
                    # self._deleteSibling(x, i, i - 1)
                    pass
                else:
                    self._deleteMerge(x, i, i - 1)
                    i -= 1
            self.delete(x.children[i], k)

    def _deleteInternalNode(self, x, k, i):
        """
        Deletes internal node
        :param x: The internal node in which key 'k' is present.
        :param k: The key to be deleted.
        :param i: The index position of key in the list
        """
        t = self.t
        # Deleting the key if the node is a leaf
        if x.leaf:
            if x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return

        # Replacing the key with its predecessor and deleting predecessor
        if len(x.children[i].keys) >= t:
            x.keys[i] = self._deletePredecessor(x.children[i])
            return
        # Replacing the key with its successor and deleting successor
        elif len(x.children[i + 1].keys) >= t:
            x.keys[i] = self._deleteSuccessor(x.children[i + 1])
            return
        # Merging the child, its left sibling and the key 'k'
        else:
            self._deleteMerge(x, i, i + 1)
            self.delete(x.children[i], k)

    def _deletePredecessor(self, x):
        """
        Deletes predecessor of key 'k' which is to be deleted
        :param x: Node
        :return: Predecessor of key 'k' which is to be deleted
        """
        if x.leaf:
            return x.keys.pop()
        n = len(x.keys) - 1
        if len(x.children[n].keys) >= self.t:
            self._deleteSibling(x, n + 1, n)
        else:
            self._deleteMerge(x, n, n + 1)
        return self._deletePredecessor(x.children[n])

    def _deleteSuccessor(self, x):
        """
        Deletes successor of key 'k' which is to be deleted
        :param x: Node
        :return: Successor of key 'k' which is to be deleted
        """
        if x.leaf:
            return x.keys.pop(0)
        if len(x.children[1].keys) >= self.t:
            self._deleteSibling(x, 0, 1)
        else:
            self._deleteMerge(x, 0, 1)
        return self._deleteSuccessor(x.children[0])

    def _deleteMerge(self, x, i, j):
        """
        Merges the children of x and one of its own keys
        :param x: Parent node
        :param i: The index of one of the children
        :param j: The index of one of the children
        """
        cNode = x.children[i]

        # Merging the x.children[i], x.children[j] and x.keys[i]
        if j > i:
            rsNode = x.children[j]
            cNode.keys.append(x.keys[i])
            # Assigning keys of right sibling node to child node
            for k in range(len(rsNode.keys)):
                cNode.keys.append(rsNode.keys[k])
                if not rsNode.leaf:
                    cNode.children.append(rsNode.children[k])
            if not rsNode.leaf:
                cNode.children.append(rsNode.children.pop())
            new = cNode
            x.keys.pop(i)
            x.children.pop(j)
        # Merging the x.children[i], x.children[j] and x.keys[i]
        else:
            lsNode = x.children[j]
            lsNode.keys.append(x.keys[j])
            # Assigning keys of left sibling node to child node
            for k in range(len(cNode.keys)):
                lsNode.keys.append(cNode.keys[k])
                if not lsNode.leaf:
                    lsNode.children.append(cNode.children[k])
            if not lsNode.leaf:
                lsNode.children.append(cNode.children.pop())
            new = lsNode
            x.keys.pop(j)
            x.children.pop(i)

        # If x is root and is empty, then re-assign root
        if x == self.root and len(x.keys) == 0:
            self.root = new

    @staticmethod
    def _deleteSibling(x, i, j):
        """
        Borrows a key from j'th child of x and appends it to i'th child of x
        :param x: Parent node
        :param i: The index of one of the children
        :param j: The index of one of the children
        """
        cNode = x.children[i]
        if i < j:
            # Borrowing key from right sibling of the child
            rsNode = x.children[j]
            cNode.keys.append(x.keys[i])
            x.keys[i] = rsNode.keys[0]
            if len(rsNode.children) > 0:
                cNode.children.append(rsNode.children[0])
                rsNode.children.pop(0)
            rsNode.keys.pop(0)
        else:
            # Borrowing key from left sibling of the child
            lsNode = x.children[j]
            cNode.keys.insert(0, x.keys[i - 1])
            x.keys[i - 1] = lsNode.keys.pop()
            if len(lsNode.children) > 0:
                cNode.children.insert(0, lsNode.children.pop())


# The main function
def main():
    B = BTree(50)

    # Insert
    customNo = 10000
    # for i in random.sample(range(customNo), customNo):
    for i in range(customNo):
        B.insert((i, f'd{i}'))
    # B.printTree(B.root)
    print()

    # Search
    for i in range(customNo):
        if B.search(i) is None:
            print("Key {} not found!".format(i))

    # Delete

#     random.setstate((3, (981115656, 2418602839, 443577728, 2488440881, 1576485378, 2397617428, 1987407892, 3374546866, 2375555002, 3344069985, 202649753, 1830848840, 4160071927, 494357230, 2163390571, 561154497, 1302311166, 26604527, 2330758703, 3610579040, 1954956342, 159074998, 1408964820, 3407667040, 1377122452, 1095138122, 2222972997, 2974813593, 202456856, 2240855892, 937492678, 2797161991, 3896165240, 1923448900, 989802926, 4078391225, 1073090866, 318877768, 1616019021, 2091256861, 524354623, 4191265629, 3122153740, 2475783104, 655592325, 1878475156, 3455510325, 2545025544, 2913830284, 2918645953, 2510327754, 1902123472, 3887257669, 205507611, 3073118752, 3299633305, 1717059702, 1362439761, 2338628671, 406586004, 1481356316, 3170229336, 2380928341, 2841098399, 2995947074, 4247610172, 2169640192, 420565449, 985354738, 1498506165, 2850884648, 1125475908, 2252688709, 2345785975, 2700842451, 2316703814, 34744642, 2865538732, 4193396264, 1728940304, 1295338672, 3993829327, 1201446833, 123991739, 1246998451, 4115282022, 451421081, 2811588270, 2135366883, 2301850514, 526898410, 4190968974, 139308154, 96416901, 3680288858, 2794667572, 63897966, 2853072663, 3600531842, 3593822346, 934352797, 2056157625, 2306303752, 2111238748, 1979854150, 892528210, 2671883118, 1443009696, 576133161, 8739712, 2000883265, 4177105853, 554226308, 931245159, 3269187783, 557028263, 1990358719, 731192896, 1608286082, 1263950143, 3255676634, 1866576456, 3355816521, 893450246, 4153008225, 115535846, 2863529348, 3410023573, 1278461727, 679214604, 3527898899, 609838095, 2157908962, 2902186506, 4009241532, 2620057367, 3467905920, 3443318411, 2006898699, 1996867245, 84171122, 54393708, 3252670214, 4152784114, 1167602169, 3448682082, 877247152, 1190409426, 1946787961, 3440093961, 398088771, 1675462380, 3292097137, 187638178, 2306528968, 2497296213, 120492361, 3987350086, 2420888385, 2153107359, 3749516492, 367130327, 391560919, 2166857859, 274909759, 1150846338, 27901473, 3689678575, 925678967, 2236943798, 837250147, 670758118, 1236437647, 510315169, 2144558404, 4000350367, 873234088, 1854636771, 1777561063, 1933782426, 1146092901, 2088786012, 568379347, 2268814420, 2979120979, 2005898097, 2594459365, 2126851554, 3008521634, 2526412346, 1147362402, 3489740135, 3673808768, 2836742513, 1915777583, 2052644318, 1507355849, 259943487, 2729952689, 3803296200, 377216075, 2273627207, 772644497, 3972140733, 1054788236, 3821110031, 3071378122, 1189375101, 990758593, 3700567106, 3033577849, 3942269473, 3451518644, 3760608811, 2569626631, 1989191893, 3143064331, 2918988612, 2265361354, 2575930067, 594410624, 280869737, 4049635738, 3696133342, 2573097363, 2812400177, 705645616, 2451101775, 3158208097, 3286673756, 129568258, 801951546, 1690171271, 842839964, 1696040878, 2251644765, 2845082102, 628872217, 1057696626, 1743823422, 4234703953, 3492185144, 2016988397, 1103431998, 106387196, 1690353701, 278048678, 3022215533, 3466675179, 3556950764, 541836464, 2116419827, 1049474984, 3085013050, 2148422585, 1506920508, 3523981692, 3320256665, 314058134, 1057527113, 846139076, 969219133, 2274031390, 183520868, 3294193217, 697437470, 1447983334, 3007037478, 1519868484, 4125506077, 4169440608, 639620101, 4284270805, 2596042068, 1963193147, 541119627, 2998165713, 1794723486, 1655754744, 1966237025, 3863727386, 2577156019, 589836345, 189395402, 728129113, 3071422866, 224361429, 3658186901, 273724310, 1980517613, 2721156842, 2285819350, 1464191555, 325699045, 1663609449, 803432196, 2894610401, 340001245, 2784011383, 3451576828, 322729816, 2572123204, 161400390, 4212404111, 2957980945, 2494557179, 2971534181, 701407825, 2050200093, 1183866879, 2418555778, 2800186680, 2481961616, 3706618832, 2637176921, 380191403, 151068306, 3751320013, 896998632, 2561356970, 2261786728, 2104610877, 1031665503, 1648857759, 805517734, 4226680943, 311693512, 2383647725, 2080924715, 2055017172, 1650852956, 2443123434, 1566496705, 1299297550, 3915587675, 2123673065, 3215999055, 107854204, 2645880596, 3322385481, 191121697, 2582422913, 2528181525, 1917800231, 1611760638, 3085494320, 1519849270, 4007388911, 1634839050, 855569845, 1100559169, 3485553775, 2934440801, 1727057936, 2700289975, 2610346978, 4051437231, 791037888, 1046673279, 2395510982, 176111893, 2119116479, 3468591306, 2332222200, 334267300, 4233772481, 3993538785, 351327539, 2589238969, 1289552739, 2614268836, 1513831089, 1157362602, 2984021521, 745837294, 701593872, 2291292490, 1726303565, 1933777127, 2896974088, 1456355653, 1317735431, 2906500438, 3967562245, 3284909468, 841482882, 57278044, 3860577260, 375210656, 2514389555, 208685089, 1470233426, 1724244052, 251600210, 1449552577, 1156539278, 140223797, 2698619381, 3879235144, 3470349793, 330045676, 2980078585, 746318671, 1074139274, 608130099, 722094966, 2315255658, 583953463, 807743079, 3139401503, 2024695001, 3567891382, 1719117616, 2553318385, 445302908, 3824456064, 3951191126, 2638718783, 1635130624, 916910809, 55367418, 727284568, 537005770, 601543940, 3244289321, 4289430610, 3667235782, 2056853655, 941084119, 2999182362, 3654233409, 1340075112, 2149299867, 1597303370, 3426199292, 2227284826, 1608659177, 2514370907, 1072194891, 629937674, 1362580010, 3182359988, 2796226290, 3748657457, 638577854, 1277781353, 2182591149, 548094563, 3704156050, 1747286509, 31585796, 1441615097, 1970787113, 83845387, 508608604, 109244566, 2084611588, 1547644377, 3408136885, 1770259861, 2460945974, 327270463, 828579161, 3903040294, 1690177284, 1147859124, 584648735, 4110759325, 2760077569, 2583536692, 3971709622, 4156341122, 3412119408, 5980955, 2763766353, 1098595010, 3104222925, 1050361880, 1941106920, 6202753, 266332072, 2957932818, 4033948511, 563570027, 1306033251, 4152199702, 409006556, 2674767202, 1804717389, 4192395518, 165565581, 913950992, 3268339848, 4041078978, 4272005918, 2863018906, 735294330, 3707155502, 3214508622, 441391490, 2687627852, 3269320687, 4059890336, 233568759, 3493520290, 1737867124, 4106480753, 4282157808, 3840718173, 4116166738, 909541362, 3203129461, 2443221875, 680175833, 409019695, 2434476982, 2803404325, 265314572, 305618133, 1310266387, 3294925942, 1030683397, 2537801603, 1319542850, 2343656931, 3881783902, 1930644029, 3402255907, 1019981349, 4011238278, 421743410, 664897853, 1833711643, 4049277795, 444416363, 3443501885, 3330316993, 2374628104, 2931281841, 1353509429, 4201993648, 1276784253, 4262421092, 2614420706, 672398499, 4019104988, 2924393107, 683458150, 1802188201, 378106166, 3584894461, 2387799193, 2990207782, 1316888793, 1170552955, 3292814911, 1848605511, 1469128850, 364810049, 123381444, 2271968483, 2622189331, 1957584246, 1986379713, 459727948, 3278456499, 628450255, 3221966696, 988110369, 3587048296, 3845915440, 3026169194, 500159655, 3789411646, 1015279984, 2763663103, 4019640595, 373881892, 232124010, 2311824521, 3546453335, 2849934542, 323537031, 1689394685, 653228905, 1706700151, 1618499189, 2906434794, 3267698507, 4010909314, 1280898492, 2221396856, 2784749850, 152243675, 1396550790, 3530546322, 3796770093, 3157062095, 2699165797, 776236954, 514509096, 3840756490, 1167789712, 2323782384, 3805221480, 3459042570, 2776422797, 286957838, 2386951598, 3322957692, 952371172, 2030186652, 1013942984, 2821388982, 1556537522, 3584336277, 3929300335, 3214357678, 748849467, 1518258759, 3546125093, 770516991, 3857814717, 359068849, 354), None)
# )
    print(random.getstate())
    sample = list(reversed(random.sample(range(customNo), customNo)))
    while len(sample):
        # i = 50
        #     print("Key {} deleted!".format(i))
        i = sample.pop()
        B.delete(B.root, (i,))
        # for i in sample:
        #     if B.search(i) is None:
        #         print("Key {} not found!".format(i))
        # B.delete(B.root, (4,))
    # Search
    for i in range(customNo):
        if B.search(i) is not None:
            print("Key {} found!".format(i))


# Program starts here
if __name__ == '__main__':
    # for _ in range(100):
    main()
