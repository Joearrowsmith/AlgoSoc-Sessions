class Signal:

    def __init__(self, order_open, order_type, signal_value,
                 single_order=True):
        self.test_signal(order_open, order_type, single_order)
        self.order_open = order_open
        self.last_order_type = None
        self.order_type = order_type
        self.value = signal_value
        self.single_order = single_order
        self.new_order = False

    def test_signal(self, order_open, order_type, single_order):
        assert order_open in [True, False]
        assert order_type in ["buy", "sell", None]
        order_not_open = (order_open is False) and (order_type is None)
        order_open = (order_open is True) and (order_type is not None)
        assert order_not_open or order_open
        assert single_order in [True, False]
        if single_order is False:
            raise NotImplementedError("Only one order can be opened \
                at a time currently.")

    def test_current_signal(self):
        self.test_signal(self.order_open, self.order_type, self.single_order)

    def set_signal_value(self, signal_value):
        self.value = signal_value

    def get_order_signal(self):
        if self.order_open:
            return self.value
        else:
            return 0

    def close(self, signal_value=None):
        if signal_value is not None:
            self.set_signal_value(signal_value)
        self.order_open = False
        self.order_type = None

    def open(self, order_type, signal_value=None):
        assert (order_type == "buy") or (order_type == "sell")
        self.check_if_new_order(order_type)
        if signal_value is not None:
            self.set_signal_value(signal_value)
        self.order_open = True
        self.last_order_type = self.order_type
        self.order_type = order_type

    def check_if_new_order(self, order_type):
        if order_type != self.order_type:
            self.new_order = True
        self.new_order = False
