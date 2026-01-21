class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        n = len(baskets)
        
        # Segment tree where each node stores the maximum capacity in that range
        # This allows us to quickly find if there's any basket with capacity >= fruit
        # We can then binary search to find the leftmost one
        
        tree = [0] * (4 * n)
        
        def build(node, start, end):
            if start == end:
                tree[node] = baskets[start]
            else:
                mid = (start + end) // 2
                build(2 * node, start, mid)
                build(2 * node + 1, mid + 1, end)
                tree[node] = max(tree[2 * node], tree[2 * node + 1])
        
        def update(node, start, end, idx, val):
            if start == end:
                tree[node] = val
            else:
                mid = (start + end) // 2
                if idx <= mid:
                    update(2 * node, start, mid, idx, val)
                else:
                    update(2 * node + 1, mid + 1, end, idx, val)
                tree[node] = max(tree[2 * node], tree[2 * node + 1])
        
        def query(node, start, end, fruit):
            # Find leftmost index in [start, end] where basket capacity >= fruit
            if tree[node] < fruit:
                return -1  # No valid basket in this range
            if start == end:
                return start
            mid = (start + end) // 2
            # Try left subtree first (to get leftmost)
            if tree[2 * node] >= fruit:
                result = query(2 * node, start, mid, fruit)
                if result != -1:
                    return result
            # Then try right subtree
            return query(2 * node + 1, mid + 1, end, fruit)
        
        build(1, 0, n - 1)
        
        unplaced = 0
        for fruit in fruits:
            idx = query(1, 0, n - 1, fruit)
            if idx == -1:
                unplaced += 1
            else:
                update(1, 0, n - 1, idx, 0)  # Mark basket as used
        
        return unplaced