"""Part 8 (agentic depth & shipping): lessons 32-35. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


LESSON_32 = (
    c.pipeline("answer")
    + c.lead(L(
        "L26 已经把 RAG 从“写死的链”升级成“会决策的循环”——单个 agent + 一条最小 workflow。但当任务本身要"
        "跨好几种<strong>能力</strong>：先<strong>查</strong>资料、再<strong>写</strong>成答复、最后<strong>核</strong>事实，"
        "把这些工具和规则<strong>全塞进一个 agent</strong>就会乱：工具一多它越容易<strong>选错</strong>，system_prompt 要"
        "同时写“怎么查 / 怎么写 / 怎么核”越写越长越<strong>打架</strong>，出错你也分不清是哪一环。这一课往前走两步："
        "① 把一个全能 agent 拆成几个<strong>各管一段</strong>的专精 agent，用 <strong>handoff（交接）</strong>把任务从一个"
        "传给下一个——<code>AgentWorkflow</code> 负责编排；② 再往底层看一层：agent 其实跑在 <strong>workflow</strong> 上，"
        "用 <code>@step</code> + 事件能把“分支 / 循环”这类<strong>控制流</strong>显式写出来——看得见、可单测。一句话：从"
        "“一个全能选手”升级到“一支有分工、会交接的小队”，并让这支小队的<strong>行进路线</strong>变成可检查的代码。",
        "L26 already upgraded RAG from a “hard-wired chain” to a “deciding loop” — one agent plus a minimal workflow. "
        "But when the task itself spans several <strong>capabilities</strong> — first <strong>search</strong> for facts, "
        "then <strong>write</strong> the reply, finally <strong>check</strong> the facts — cramming all those tools and "
        "rules <strong>into one agent</strong> gets messy: with many tools it more easily <strong>picks wrong</strong>, "
        "its system prompt has to say “how to search / write / check” all at once, growing long and "
        "<strong>self-contradictory</strong>, and on a failure you can't tell which part broke. This lesson takes two "
        "steps forward: (1) split one do-everything agent into several specialized agents that <strong>each own one "
        "slice</strong>, and use <strong>handoff</strong> to pass the task from one to the next — with "
        "<code>AgentWorkflow</code> doing the orchestration; (2) look one layer deeper: an agent actually runs on a "
        "<strong>workflow</strong>, and with <code>@step</code> + events you can write <strong>control flow</strong> "
        "like “branches / loops” out explicitly — visible and unit-testable. In a line: upgrade from “one all-round "
        "player” to “a small team with clear roles that hands off”, and make that team's <strong>route</strong> "
        "inspectable code.",
    ))
    + d.compare2(
        (L("单 agent 全包", "One agent does it all"), i18n.render(L(
            "查 / 写 / 核的工具和规则<strong>全塞进一个</strong> agent：工具一多就<strong>选错</strong>，system_prompt 越写"
            "越长越<strong>打架</strong>，出错也分不清是哪一环。",
            "all the search / write / check tools and rules <strong>crammed into one</strong> agent: many tools mean "
            "<strong>wrong picks</strong>, the system prompt grows long and <strong>self-contradictory</strong>, and "
            "failures are hard to localize."))),
        (L("多 agent 分工 + handoff", "Many agents: split + handoff"), i18n.render(L(
            "每个 agent <strong>只精一段</strong>、只配该段工具；干完用 <strong>handoff</strong> 把任务交给下一个更合适的"
            "——<strong>清晰、好测、好扩</strong>。",
            "each agent <strong>masters one slice</strong> with only that slice's tools; when done it <strong>hands "
            "off</strong> to the next, more suitable one — <strong>clear, testable, extensible</strong>."))),
        caption=L("把“一个全能 agent”拆成“分工 + 会交接的小队”：窄职责更准，交接路线显式可控",
                  "Split “one do-everything agent” into “roles + a handing-off team”: narrow duties are more accurate, handoff routes explicit and controlled"),
    )
    + c.section(
        L("① 单 agent 不够：拆成多 agent 分工 + 交接(handoff)",
          "① One agent isn't enough: split into multiple agents with division of labor + handoff"),
        L(
            "L26 的单 agent 已经会“看问题、选工具、循环到够答”。但当任务要跨好几种能力，把工具和规则全堆在一个 agent 上，"
            "麻烦就来了：工具一多，它得在十几个里挑，<strong>选错的概率上升</strong>；system_prompt 要同时交代“怎么查、"
            "怎么写、怎么核”，越写越长、彼此<strong>打架</strong>，模型<strong>顾此失彼</strong>；真出了错，你也分不清是"
            "“查错了”还是“写跑了”。解法是<strong>分工</strong>：把一个全能 agent 拆成几个<strong>各管一段</strong>的专精 "
            "agent，每个只配<strong>它那段需要的工具</strong>、只写<strong>它那段的 system_prompt</strong>——窄而精，"
            "自然更准、更好维护。它们之间靠 <strong>handoff（交接）</strong>协作：一个 agent 干完自己那段，把<strong>控制权"
            "连同上下文</strong>交给下一个更合适的 agent，像接力赛传棒（查→写→核三个角色就能串成一条线）。要点是：handoff "
            "<strong>不是</strong>“关掉某个工具”，<strong>也不是</strong>“换个更大的模型”，而是把<strong>任务移交给队友</strong>。",
            "L26's single agent already “reads the question, picks a tool, and loops until it can answer”. But when the "
            "task spans several capabilities, piling all the tools and rules onto one agent invites trouble: with many "
            "tools it must choose among a dozen, so <strong>the odds of a wrong pick rise</strong>; the system prompt "
            "has to spell out “how to search, write, and check” at once, growing long and <strong>self-contradictory"
            "</strong> until the model is <strong>pulled every way</strong>; and when something breaks you can't tell "
            "whether it “searched wrong” or “wrote off-track”. The fix is <strong>division of labor</strong>: split one "
            "do-everything agent into several specialized agents that <strong>each own one slice</strong>, each wired "
            "only with <strong>the tools its slice needs</strong> and only <strong>its slice's system prompt</strong> — "
            "narrow and sharp, naturally more accurate and easier to maintain. They cooperate via <strong>handoff"
            "</strong>: one agent finishes its slice and passes <strong>control along with the context</strong> to the "
            "next, more suitable agent, like a relay baton (search→write→check threads three roles into one line). The "
            "point: a handoff is <strong>not</strong> “turning off a tool” and <strong>not</strong> “switching to a "
            "bigger model” — it is <strong>handing the task to a teammate</strong>.",
        ),
    )
    + c.section(
        L("② <code>AgentWorkflow</code> 编排多 agent：name / system_prompt / tools / can_handoff_to",
          "② <code>AgentWorkflow</code> orchestrates the agents: name / system_prompt / tools / can_handoff_to"),
        L(
            "把这支小队<strong>编排</strong>起来的，是 <code>AgentWorkflow</code>。每个成员是一个 <code>FunctionAgent</code>，"
            "四样东西定义它的角色：<strong>name</strong>（队友靠名字点名交接）、<strong>system_prompt</strong>（它这段的"
            "职责与风格）、<strong>tools</strong>（它能用的工具，撰稿 agent 可以一个都不带）、<strong>can_handoff_to"
            "</strong>（它<strong>允许</strong>把任务交给哪些 agent——交接路线是你<strong>显式声明</strong>的，不是模型乱传）。"
            "构造时把所有 agent 放进 <code>agents=[...]</code>，再指定 <strong>root_agent</strong> 作为<strong>入口</strong>"
            "（第一个接手的人）。运行 <code>await workflow.run(user_msg=...)</code>，root agent 先处理，需要时<strong>调用"
            "一次 handoff</strong> 把任务交给下一位——其实 handoff 在底层就是框架<strong>自动注入的一个工具</strong>，所以"
            "“交接”和 L26 的“调用工具”<strong>本质同源</strong>，只不过这次被调用的“工具”是<strong>另一个 agent</strong>。"
            "（这也正好踩在 L31 的砖上：让模型可靠产出“受约束的结构”，就是工具调用、也是 handoff 的地基。）",
            "What <strong>orchestrates</strong> this team is <code>AgentWorkflow</code>. Each member is a "
            "<code>FunctionAgent</code> defined by four things: <strong>name</strong> (teammates hand off by name), "
            "<strong>system_prompt</strong> (its slice's duty and style), <strong>tools</strong> (the tools it may use "
            "— a writing agent can carry none), and <strong>can_handoff_to</strong> (which agents it is <strong>allowed"
            "</strong> to pass the task to — the handoff routes are <strong>declared by you</strong>, not improvised by "
            "the model). You put all agents into <code>agents=[...]</code> and name a <strong>root_agent</strong> as the "
            "<strong>entry</strong> (whoever takes the task first). Calling <code>await workflow.run(user_msg=...)</code>, "
            "the root agent handles it first and, when needed, <strong>invokes one handoff</strong> to pass the task on "
            "— under the hood a handoff is just a <strong>tool the framework auto-injects</strong>, so “handing off” and "
            "L26's “calling a tool” <strong>share the same root</strong>; it's only that this time the “tool” being "
            "called is <strong>another agent</strong>. (This stands on L31's brick: making the model reliably emit a "
            "“constrained structure” is the bedrock of both tool calls and handoffs.)",
        ),
    )
    + c.code(
        "from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent\n\n"
        'research = FunctionAgent(name="research", description="查资料的研究员", tools=[search_tool], llm=llm,\n'
        '                         system_prompt="查资料，把要点交给 writer", can_handoff_to=["write"])\n'
        'write = FunctionAgent(name="write", description="根据要点写草稿的写手", tools=[], llm=llm,\n'
        '                      system_prompt="据要点写成草稿，交给 reviewer", can_handoff_to=["review"])\n'
        'review = FunctionAgent(name="review", description="复核定稿的把关人", tools=[], llm=llm,\n'
        '                       system_prompt="复核草稿，通过则定稿", can_handoff_to=[])\n'
        'workflow = AgentWorkflow(agents=[research, write, review], root_agent="research")\n'
        'resp = await workflow.run(user_msg="写一段关于 X-2000 的简报")',
        caption=L("三个专精 agent + handoff 链：research 查完交给 write 写草稿、write 再交给 review 复核定稿；AgentWorkflow 编排，root_agent 是入口；多 agent 下每个都要 description（handoff 据此择人）",
                  "Three specialized agents + a handoff chain: research gathers and hands to write for a draft, write then hands to review to finalize; AgentWorkflow orchestrates, root_agent is the entry; in a multi-agent workflow each agent needs a description (handoff targets are chosen by it)"),
    )
    + c.source_ref(
        "agent/workflow/multi_agent_workflow.py", "AgentWorkflow",
        L("编排多个 agent 协作与交接(handoff)。", "orchestrates multiple agents with handoffs."),
    )
    + d.flow([
        ("user", L("用户问题", "user query")),
        ("research", L("research agent", "research agent"), L("查资料", "gathers facts")),
        ("write", L("write agent", "write agent"), L("handoff 后写答", "writes after handoff")),
        ("review", L("review agent", "review agent"), L("复核把关", "checks")),
    ], caption=L("多智能体：按角色分工，用 handoff 把任务交给下一个专家",
                 "multi-agent: split by role, hand off the task to the next specialist"))
    + c.section(
        L("③ 底层是 workflow：<code>@step</code> + 事件，把分支 / 循环显式写出来",
          "③ Underneath is a workflow: <code>@step</code> + events make branches / loops explicit"),
        L(
            "再往下看一层：L26 说过，<strong>agent 其实是一个内置了“工具循环”的 workflow</strong>。<code>AgentWorkflow</code> "
            "把这套循环和 handoff 都封好了，开箱即用。但当你要的<strong>控制流</strong>不只是“循环调工具”——比如“<strong>"
            "琐碎问题直接答、复杂问题才检索</strong>”这种<strong>分支</strong>，或“<strong>没检索够就回到检索再来一轮</strong>”"
            "这种<strong>循环</strong>——就可以<strong>落到裸 <code>Workflow</code></strong>，亲手把流程画清楚。写法承接 L26 的"
            "最小 workflow：每个 <code>@step</code> 方法<strong>吃一种事件、返回一种事件</strong>，<code>StartEvent</code> 进、"
            "<code>StopEvent</code> 出。关键升级在<strong>返回类型</strong>：当一个 step 的返回标成 <code>Retrieved | "
            "StopEvent</code>（联合类型），就等于声明“我这步<strong>会分叉</strong>——可能往下检索，也可能直接收尾”，框架"
            "据此把<strong>分支连进流程图</strong>。于是控制流不再藏在一长串 <code>if/else</code> 里，而是<strong>变成显式的"
            "事件流转</strong>：每个 step 是个<strong>纯函数式的小盒子</strong>（收什么、发什么一目了然），可以<strong>单独"
            "测试</strong>，分支和循环都<strong>画得出、测得到</strong>——这正是比“写死一个大函数”更可控的地方。",
            "Drop one more layer: as L26 noted, <strong>an agent is really a workflow with a built-in “tool loop”</strong>. "
            "<code>AgentWorkflow</code> packages that loop and the handoffs for you, ready out of the box. But when the "
            "<strong>control flow</strong> you want is more than “loop and call tools” — say a <strong>branch</strong> "
            "like “<strong>answer trivial questions directly, retrieve only for complex ones</strong>”, or a "
            "<strong>loop</strong> like “<strong>if retrieval wasn't enough, go back and retrieve again</strong>” — you "
            "can <strong>drop to a raw <code>Workflow</code></strong> and draw the flow by hand. The style continues "
            "L26's minimal workflow: each <code>@step</code> method <strong>consumes one event and returns one</strong>, "
            "<code>StartEvent</code> in, <code>StopEvent</code> out. The key upgrade is the <strong>return type</strong>: "
            "when a step is annotated to return <code>Retrieved | StopEvent</code> (a union), it declares “this step "
            "<strong>forks</strong> — it may retrieve or finish right here”, and the framework <strong>wires that branch "
            "into the graph</strong>. So control flow no longer hides inside a long <code>if/else</code>; it "
            "<strong>becomes an explicit flow of events</strong>: each step is a <strong>small functional box</strong> "
            "(clear about what it takes and emits), <strong>testable in isolation</strong>, with branches and loops you "
            "can <strong>draw and test</strong> — exactly what makes it more controllable than “one big hard-wired "
            "function”.",
        ),
    )
    + c.code(
        "from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event\n\n"
        "class Retrieved(Event):\n"
        "    nodes: list\n\n"
        "class RAGFlow(Workflow):\n"
        "    @step\n"
        "    async def route(self, ev: StartEvent) -&gt; Retrieved | StopEvent:\n"
        "        if is_trivial(ev.query):\n"
        '            return StopEvent(result="直接答，无需检索")   # 分支：跳过检索\n'
        "        return Retrieved(nodes=retrieve(ev.query))",
        caption=L("裸 Workflow：route 这个 @step 按问题难易返回不同事件（Retrieved 或 StopEvent）——分支被写成了可见、可测的控制流",
                  "Raw Workflow: the route @step returns different events by difficulty (Retrieved or StopEvent) — the branch becomes visible, testable control flow"),
    )
    + d.vflow([
        (L("StartEvent 进入", "StartEvent in"), L("路由 @step", "router @step")),
        (L("分支：琐碎问题 → StopEvent 直接答", "branch: trivial → StopEvent"),),
        (L("否则 → Retrieved 事件 → 合成 @step", "else → Retrieved → synth @step"),),
        (L("StopEvent 出", "StopEvent out"),),
    ], caption=L("workflow 用事件显式表达分支/循环——控制流看得见、可测",
                 "a workflow makes branches/loops explicit as events — visible, testable control flow"))
    + c.section(
        L("④ 取舍：越多 agent / 越自由越强，但越难调、越贵",
          "④ Trade-off: more agents / more freedom is stronger, but harder to debug and pricier"),
        L(
            "能力越强，代价越实。<strong>每多一个 agent、每一次 handoff，都是又一次 LLM 决策</strong>：更多 token、更高延迟，"
            "还多了“<strong>会不会交错人、会不会在两个 agent 间反复踢皮球</strong>”这种新失败点。多 agent 也<strong>更难调"
            "</strong>——出了错你得先弄清“是哪个 agent、在哪一步、为什么这么交接”，这让 L23 的 <strong>trace 从“锦上添花”"
            "变成“必需品”</strong>。所以延续 L26 的那把尺子，按需选<strong>最低自主度</strong>：<strong>固定管道 → 单 agent → "
            "多 agent / 裸 workflow</strong>，一级不够再上一级。判断要不要拆多 agent，就看任务<strong>能不能按角色清晰切开"
            "</strong>：能（查 / 写 / 核各管一段、要交接），拆了更清晰更好测；不能（其实一个角色几个工具就够），拆了只是徒增 "
            "handoff 的成本与不确定。一句话：<strong>先用最简单能解的那个</strong>。",
            "The more capable, the realer the cost. <strong>Every extra agent and every handoff is another LLM decision"
            "</strong>: more tokens, higher latency, plus new failure modes — “<strong>did it hand off to the wrong one"
            "</strong>” and “<strong>are two agents ping-ponging the task back and forth</strong>”. Multi-agent is also "
            "<strong>harder to debug</strong> — on a failure you must first work out “which agent, at which step, and why "
            "it handed off that way”, which turns L23's <strong>tracing from a nice-to-have into a must-have</strong>. So "
            "keep L26's yardstick and pick the <strong>lowest autonomy</strong> that works: <strong>fixed pipeline → "
            "single agent → multi-agent / raw workflow</strong>, climbing only when a rung isn't enough. To decide whether "
            "to split into multiple agents, ask whether the task <strong>cuts cleanly along roles</strong>: if it does "
            "(search / write / check each owning a slice, with handoffs), splitting is clearer and more testable; if it "
            "doesn't (one role with a few tools really suffices), splitting just adds handoff cost and uncertainty. In a "
            "line: <strong>use the simplest thing that solves it</strong>.",
        ),
        c.compare_table(
            [L("对比项", "Aspect"), L("单 agent（L26）", "Single agent (L26)"),
             L("多 agent · AgentWorkflow", "Multi-agent · AgentWorkflow"),
             L("裸 Workflow · @step", "Raw Workflow · @step")],
            [
                [L("适合", "Best for"), L("一个角色、几个工具够用", "one role, a few tools suffice"),
                 L("任务能按角色清晰拆分、要交接", "task splits cleanly by role, needs handoffs"),
                 L("要显式的分支 / 循环 / 并行控制流", "explicit branch / loop / parallel control flow")],
                [L("怎么协作", "How they cooperate"), L("内置工具循环", "a built-in tool loop"),
                 L("handoff 在 agent 间传任务", "handoff passes the task between agents"),
                 L("事件在 @step 间流转", "events flow between @steps")],
                [L("控制流", "Control flow"), L("藏在工具循环里", "hidden in the tool loop"),
                 L("交接路线由 can_handoff_to 声明", "handoff routes declared via can_handoff_to"),
                 L("显式可见：联合返回即分支", "explicit, visible: a union return is a branch")],
                [L("代价", "Cost"), L("多轮工具调用", "multiple tool-calling turns"),
                 L("每次 handoff 多一次 LLM 决策、更难追谁干的", "each handoff is one more LLM decision; harder to trace who did what"),
                 L("要自己写事件连线，但最可控可测", "you wire the events yourself, but it's the most controllable and testable")],
            ],
        ),
    )
    + c.analogy(L(
        "单 agent 像一个<strong>样样都会的全能选手</strong>：一个人要查资料、写稿、还要自己校对，事情一多就顾此失彼。"
        "多 agent 像一支<strong>有分工的小队</strong>：调研员只管查、撰稿员只管写、审校员只管挑错，每人手里的活窄而精，"
        "干完自己那段就把<strong>接力棒（handoff）</strong>连同笔记交给下一位。而 workflow 就像这支小队<strong>写在白板上"
        "的流程图</strong>：先做什么、什么情况下跳过哪步、什么情况下返工重来——路线画明白了，哪一步出问题一眼就能定位，"
        "也能单独演练。",
        "A single agent is like <strong>one all-round player</strong> who must research, draft, and proofread alone — "
        "overwhelmed once there's a lot to do. Multi-agent is like <strong>a team with clear roles</strong>: the "
        "researcher only gathers, the writer only writes, the reviewer only catches mistakes; each person's slice is "
        "narrow and sharp, and when done they pass the <strong>baton (handoff)</strong> — along with their notes — to "
        "the next. A workflow is that team's <strong>flowchart on a whiteboard</strong>: what to do first, when to skip a "
        "step, when to loop back and redo — with the route drawn out, you can spot exactly where a step breaks and even "
        "rehearse it in isolation.",
    ))
    + c.key_points([
        L("单 agent 工具 / 职责堆太多就乱；拆成<strong>多个专精 agent</strong>、用 <strong>handoff（交接）</strong>把任务传给"
          "下一个更合适的。",
          "One agent with too many tools / duties gets messy; split into <strong>multiple specialized agents</strong> and "
          "use <strong>handoff</strong> to pass the task to the next, more suitable one."),
        L("<strong>AgentWorkflow</strong> 编排多 agent：每个 <code>FunctionAgent</code> 有 <code>name</code> / "
          "<code>system_prompt</code> / <code>tools</code> / <code>can_handoff_to</code>，<code>root_agent</code> 是入口。",
          "<strong>AgentWorkflow</strong> orchestrates the agents: each <code>FunctionAgent</code> has <code>name</code> / "
          "<code>system_prompt</code> / <code>tools</code> / <code>can_handoff_to</code>, and <code>root_agent</code> is "
          "the entry."),
        L("agent 底层跑在 <strong>workflow</strong> 上；用 <code>@step</code> + 事件把<strong>分支 / 循环</strong>这类控制流"
          "<strong>显式</strong>写出来——看得见、每步可单测（联合返回类型即分支）。",
          "An agent runs on a <strong>workflow</strong>; use <code>@step</code> + events to make control flow like "
          "<strong>branches / loops</strong> <strong>explicit</strong> — visible and unit-testable per step (a union "
          "return type is a branch)."),
        L("取舍：agent 越多、越自由越强，但每次 handoff 多一次 LLM 决策——<strong>更慢、更贵、更难调</strong>；<strong>先用"
          "最简能解的</strong>（固定管道 → 单 agent → 多 agent）。",
          "Trade-off: more agents and more freedom are stronger, but each handoff is another LLM decision — "
          "<strong>slower, pricier, harder to debug</strong>; <strong>use the simplest thing that works</strong> (fixed "
          "pipeline → single agent → multi-agent)."),
    ])
    + c.design_highlight(L(
        "多智能体与控制流的精髓，是把 L26 的“一个会决策的 agent”再<strong>拆开</strong>、再<strong>摊平</strong>：<strong>"
        "拆开</strong>成一支<strong>有分工、会 handoff 的小队</strong>（<code>AgentWorkflow</code> 编排，每个 agent 只精一段、"
        "按 <code>can_handoff_to</code> 把任务交给下一位），<strong>摊平</strong>成一张<strong>显式的事件流程图</strong>"
        "（裸 <code>Workflow</code> 用 <code>@step</code> + 事件把分支 / 循环写成看得见、可单测的控制流）。两步都在解同一个"
        "问题：当任务复杂到一个 agent 的提示词和工具都装不下时，<strong>与其把复杂性塞进一个黑箱，不如把它拆成可命名、"
        "可观测、可测试的小块</strong>。但更强从来不是免费的——<strong>多一个 agent 就多一次 LLM 决策、多一处可能跑偏</strong>，"
        "调试也从“看一个 agent”变成“看一支队伍怎么交接”，因此越 agentic 越离不开 L23 的 trace。真正的判断不是“能不能上多 "
        "agent”，而是“<strong>这个任务配不配得上多 agent 的代价</strong>”：能按角色干净拆开、且确实需要交接，才拆；否则一个 "
        "agent、甚至一条固定管道，往往又快又稳。还有一道绕不开的关：当这支自由的小队要去<strong>删数据、下订单、发邮件</strong>"
        "这类<strong>高风险动作</strong>时，光靠它们自己拍板就太冒险了——得有人能<strong>在回路里</strong>喊停、点头确认。那正是"
        "下一课 <strong>L33 人在回路（HITL）</strong>要补上的“刹车”。",
        "The essence of multi-agent and control flow is to take L26's “one deciding agent” and both <strong>split it "
        "apart</strong> and <strong>flatten it out</strong>: <strong>split</strong> into a <strong>team with roles that "
        "hands off</strong> (<code>AgentWorkflow</code> orchestrates; each agent masters one slice and passes the task on "
        "per <code>can_handoff_to</code>), and <strong>flatten</strong> into an <strong>explicit event flowchart</strong> "
        "(a raw <code>Workflow</code> uses <code>@step</code> + events to write branches / loops as visible, "
        "unit-testable control flow). Both moves solve the same problem: when a task grows too complex for one agent's "
        "prompt and tools to hold, <strong>rather than stuffing the complexity into one black box, break it into named, "
        "observable, testable pieces</strong>. But more power is never free — <strong>each extra agent is another LLM "
        "decision and another place to drift</strong>, and debugging shifts from “watching one agent” to “watching a team "
        "hand off”, so the more agentic you go, the more you lean on L23's tracing. The real call isn't “can we use "
        "multi-agent” but “<strong>is this task worth multi-agent's cost</strong>”: split only when the work cuts cleanly "
        "along roles and genuinely needs handoffs; otherwise a single agent — or even a fixed pipeline — is often faster "
        "and steadier. And one gate is unavoidable: when this free-roaming team goes to <strong>delete data, place "
        "orders, or send email</strong> — <strong>high-risk actions</strong> — letting them decide alone is too risky; "
        "someone must be able to <strong>step into the loop</strong>, halt, and confirm. That's the “brake” the next "
        "lesson, <strong>L33 Human-in-the-Loop (HITL)</strong>, adds.",
    ))
)
LESSON_33 = (
    c.pipeline("answer")
    + c.lead(L(
        "上一课的多 agent 小队很能干，也很<strong>自由</strong>——它可能自己决定去<strong>删库、转账、下单、对外发"
        "消息</strong>。这些动作<strong>不可逆</strong>：错了就收不回来，光靠模型自己拍板太冒险。<strong>人在回路"
        "（HITL）</strong>就是给这种高风险动作装一道<strong>刹车</strong>：在真正动手前<strong>暂停</strong>，把请求交给"
        "人，<strong>等人点头</strong>才继续、摇头就中止。关键不是“每一步都要人盯”——那会把系统<strong>拖垮</strong>——"
        "而是<strong>只在不可逆 / 高风险的那一步加闸</strong>，其余照常自动。LlamaIndex 把这件事做得很轻：workflow 里"
        "某个 <code>@step</code> <strong>返回</strong>一个 <code>InputRequiredEvent</code> 就自动“挂起并向人请求输入”，"
        "调用方从事件流里取到它、回一个 <code>HumanResponseEvent</code>，消费该事件的 <code>@step</code> 据此恢复或"
        "中止——一来一回，干净利落。",
        "Last lesson's multi-agent team is capable — and very <strong>free</strong>: it might decide on its own to "
        "<strong>drop a database, transfer money, place an order, or message the outside world</strong>. Those actions "
        "are <strong>irreversible</strong>: once wrong you can't take them back, and letting the model alone make the "
        "call is too risky. <strong>Human-in-the-loop (HITL)</strong> puts a <strong>brake</strong> on such high-risk "
        "actions: <strong>pause</strong> right before acting, hand the request to a human, and continue only on a "
        "<strong>yes</strong> — abort on a no. The point is <strong>not</strong> “a human watches every step” — that "
        "would <strong>grind the system to a halt</strong> — but to <strong>gate only the irreversible / high-risk "
        "step</strong>, leaving the rest automatic. LlamaIndex makes this light: a <code>@step</code> in a workflow that "
        "<strong>returns</strong> an <code>InputRequiredEvent</code> automatically “pauses and asks a human”; the caller "
        "picks it up from the event stream and sends back a <code>HumanResponseEvent</code>, and the <code>@step</code> "
        "consuming that event resumes or aborts — a clean round-trip.",
    ))
    + d.compare2(
        (L("全自动", "Fully automatic"), i18n.render(L("快，但删错/下错单<strong>无法挽回</strong>",
                                                      "fast, but a wrong delete/order is <strong>irreversible</strong>"))),
        (L("关键步加闸", "Gate the risky step"), i18n.render(L("仅高风险动作要人确认，其余自动",
                                                            "only high-risk actions need a human; the rest stays automatic"))),
        caption=L("不是所有步都要人——只在<strong>不可逆/高风险</strong>处加闸",
                  "not every step needs a human — gate only the <strong>irreversible/high-risk</strong> ones"),
    )
    + c.section(
        L("① 为什么要人在回路：高风险 / 不可逆动作不能全自动",
          "① Why human-in-the-loop: high-risk / irreversible actions can't be fully automatic"),
        L(
            "L32 的小队越自由就越能干，但<strong>LLM 是概率的</strong>——它总有选错的时候。对<strong>大多数动作</strong>"
            "（读文档、起草文字、再查一次资料）来说，选错的代价很低：<strong>重试一次</strong>就好，没人受伤。可有一类"
            "动作会<strong>越过边界、落到真实世界</strong>：<strong>删库、转账、下单、对外发邮件 / 发消息</strong>——它们"
            "<strong>不可逆</strong>，一旦做错就<strong>收不回来</strong>，可能是真金白银的损失或对外的事故。正因如此，"
            "<strong>恰恰在这些点上</strong>不能让自主权独自拍板。HITL 的思路很简单：在<strong>不可逆的那一步前</strong>"
            "插入一个人，让人来做<strong>最后的批准</strong>。但人不是免费的——每一次确认都<strong>加延迟、打扰人"
            "</strong>，所以只把它放在<strong>代价最高、最不可逆</strong>的动作上；其余一切照常自动。这正是上一课结尾"
            "留下的那道“刹车”。",
            "L32's team grows more capable as it grows freer, but <strong>an LLM is probabilistic</strong> — it will "
            "sometimes pick wrong. For <strong>most actions</strong> (reading a doc, drafting text, one more lookup) a "
            "wrong pick is cheap: just <strong>retry</strong>, no one gets hurt. But one class of action <strong>crosses "
            "the boundary into the real world</strong>: <strong>dropping a database, transferring money, placing an "
            "order, sending outbound email / messages</strong> — these are <strong>irreversible</strong>; once done "
            "wrong you <strong>can't take them back</strong>, and the loss can be real money or an outward-facing "
            "incident. That is exactly why, <strong>at those points</strong>, autonomy must not decide alone. HITL's idea "
            "is simple: insert a human <strong>right before the irreversible step</strong> and let them give the "
            "<strong>final approval</strong>. But a human isn't free — every confirmation <strong>adds latency and "
            "interrupts someone</strong> — so you reserve it for the <strong>costliest, least reversible</strong> "
            "actions and keep everything else automatic. This is the very “brake” the last lesson left off on.",
        ),
    )
    + c.section(
        L("② 机制：<code>@step</code> 返回 <code>InputRequiredEvent</code> 挂起，调用方回 <code>HumanResponseEvent</code> 恢复",
          "② Mechanism: a <code>@step</code> returns <code>InputRequiredEvent</code> to pause; the caller sends "
          "<code>HumanResponseEvent</code> to resume"),
        L(
            "承接 L32 的底层视角：agent 跑在 <strong>workflow</strong> 上，流程由 <code>@step</code> + <strong>事件"
            "</strong>驱动。HITL 用的就是这套机器，只多了一对<strong>专门的事件</strong>，机制分两半、正好一来一回。"
            "<strong>① workflow 侧——挂起</strong>：某个 <code>@step</code> 在要动手前，把返回类型标成 "
            "<code>InputRequiredEvent</code> 并<strong>返回</strong>它。框架会<strong>自动把它写进事件流</strong>，而且"
            "<strong>不需要任何下游 step 去消费</strong>就能通过校验——于是流程<strong>停在这里、向人请求输入</strong>。"
            "<code>InputRequiredEvent(prefix=\"…\")</code> 里的 <strong>prefix</strong> 就是要展示给人看的那句话"
            "（“确认要删账户吗？”）。<strong>② 调用方侧——回灌</strong>：发起 workflow 的人正用 "
            "<code>async for ev in handler.stream_events()</code> <strong>盯着事件流</strong>；一旦看到 "
            "<code>InputRequiredEvent</code>，就拿 <code>ev.prefix</code> 去问真正的人（前端弹窗 / 审批系统 / 命令行），"
            "把人的回答<strong>装进</strong> <code>HumanResponseEvent(response=…)</code>，用 "
            "<code>handler.ctx.send_event(...)</code> <strong>送回</strong> workflow。消费 <code>HumanResponseEvent"
            "</code> 的那个 <code>@step</code> 随即<strong>被唤醒</strong>，读 <code>ev.response</code>，据此<strong>恢复"
            "或中止</strong>。一句话：<strong>workflow 返回 <code>InputRequiredEvent</code>、调用方流式取到再送回 "
            "<code>HumanResponseEvent</code></strong>，这“出—回”两步就是 HITL 的全部——<code>prefix</code> 把问题"
            "带出去，<code>response</code> 把人的决定带回来。",
            "Continuing L32's under-the-hood view: an agent runs on a <strong>workflow</strong>, driven by "
            "<code>@step</code> + <strong>events</strong>. HITL uses that same machinery, plus one <strong>dedicated "
            "pair of events</strong>; the mechanism is two halves — exactly one round-trip. <strong>(1) Workflow side — "
            "pause</strong>: right before acting, a <code>@step</code> annotates its return as "
            "<code>InputRequiredEvent</code> and <strong>returns</strong> it. The framework <strong>auto-writes it to "
            "the event stream</strong>, and it <strong>needs no downstream step to consume it</strong> to pass "
            "validation — so the flow <strong>stops here and asks a human</strong>. The <strong>prefix</strong> in "
            "<code>InputRequiredEvent(prefix=\"…\")</code> is the line to show the human (“confirm deleting the "
            "account?”). <strong>(2) Caller side — inject back</strong>: whoever launched the workflow is "
            "<strong>watching the stream</strong> with <code>async for ev in handler.stream_events()</code>; on seeing "
            "an <code>InputRequiredEvent</code>, it takes <code>ev.prefix</code> to ask a real human (a frontend dialog "
            "/ approval system / CLI), wraps the answer in <code>HumanResponseEvent(response=…)</code>, and <strong>sends "
            "it back</strong> with <code>handler.ctx.send_event(...)</code>. The <code>@step</code> consuming "
            "<code>HumanResponseEvent</code> then <strong>wakes up</strong>, reads <code>ev.response</code>, and "
            "<strong>resumes or aborts</strong> accordingly. In a line: <strong>the workflow returns "
            "<code>InputRequiredEvent</code>, and the caller streams it and sends back "
            "<code>HumanResponseEvent</code></strong> — that “out-and-back” pair is all of HITL: <code>prefix</code> "
            "carries the question out, <code>response</code> carries the human's decision back.",
        ),
    )
    + c.code(
        "from llama_index.core.workflow import (Workflow, step, StartEvent, StopEvent,\n"
        "                                        InputRequiredEvent, HumanResponseEvent)\n\n"
        "class ApprovalFlow(Workflow):\n"
        "    @step\n"
        "    async def act(self, ev: StartEvent) -&gt; InputRequiredEvent:\n"
        "        return InputRequiredEvent(prefix=\"确认要执行『删除账户』吗？(yes/no) \")   # 写入事件流并挂起\n\n"
        "    @step\n"
        "    async def finish(self, ev: HumanResponseEvent) -&gt; StopEvent:\n"
        "        ok = ev.response.strip().lower() == \"yes\"\n"
        "        return StopEvent(result=\"已执行\" if ok else \"已取消\")",
        caption=L("workflow 侧：act 这个 @step 返回 InputRequiredEvent——自动写入事件流并挂起；消费 HumanResponseEvent 的 finish 据 response 恢复或中止",
                  "Workflow side: the act @step returns InputRequiredEvent — auto-written to the stream and pausing; finish, which consumes HumanResponseEvent, resumes or aborts on response"),
    )
    + c.code(
        "handler = ApprovalFlow().run()\n"
        "async for ev in handler.stream_events():\n"
        "    if isinstance(ev, InputRequiredEvent):\n"
        "        answer = input(ev.prefix)                              # 真实场景：来自前端/审批系统\n"
        "        handler.ctx.send_event(HumanResponseEvent(response=answer))\n"
        "result = await handler",
        caption=L("调用方侧：流式监听事件流，遇到 InputRequiredEvent 就拿 prefix 去问人，把答案装进 HumanResponseEvent 送回——await handler 取最终结果",
                  "Caller side: stream the events; on InputRequiredEvent, use prefix to ask a human, wrap the answer in HumanResponseEvent and send it back — await handler for the result"),
    )
    + c.source_ref(
        "workflow/__init__.py", "InputRequiredEvent / HumanResponseEvent",
        L("workflow 暂停向人请求输入，拿到回应再继续。",
          "the workflow pauses to ask a human, then resumes on their response."),
    )
    + d.flow([
        ("act", L("准备高风险动作", "about to act")),
        ("ask", L("发 InputRequired", "emit InputRequired"), L("挂起等待", "pause &amp; wait")),
        ("human", L("人确认", "human decides"), L("yes / no", "yes / no")),
        ("done", L("继续 / 中止", "continue / abort")),
    ], active="ask", caption=L("人在回路：危险动作前暂停，拿到人的确认再继续",
                               "HITL: pause before a risky action, resume only on human confirmation"))
    + c.section(
        L("③ 落点：审批闸、低置信度兜底、敏感工具调用前确认",
          "③ Where it lands: approval gates, low-confidence fallback, confirming before sensitive tool calls"),
        L(
            "HITL 在三处最常落地，但都遵循同一条线——<strong>只在该加闸的地方加闸</strong>。<strong>① 审批闸</strong>："
            "在<strong>不可逆的对外动作</strong>前（删库 / 转账 / 下单 / 群发）强制一次<strong>人工 yes/no</strong>，就像"
            "上面的 <code>ApprovalFlow</code>——通过才执行，否则中止。<strong>② 低置信度兜底</strong>：当模型 / 检索"
            "<strong>没把握</strong>时（相似度过低、证据互相矛盾、模型自陈“不确定”），<strong>别硬编</strong>，转人工"
            "裁决；关键是设<strong>阈值</strong>——只有<strong>置信度低于线</strong>才弹给人，高置信的照常自动答，别让 "
            "HITL 变成“凡事都问”。<strong>③ 敏感工具调用前确认</strong>：给 agent 的工具<strong>分级</strong>——把 "
            "<code>send_email</code> / <code>run_sql</code> / <code>place_order</code> 标成“敏感”，agent <strong>真要"
            "调用前</strong>暂停让人点头；而只读 / 可撤销的工具（检索、查天气）<strong>放它自己跑</strong>。三者都在解"
            "同一个问题：把<strong>极少数</strong>不可逆 / 高风险 / 低置信的点<strong>拦下来交给人</strong>，其余维持"
            "自动——这也正好接上 L25 的护栏（护栏<strong>自动挡掉明显违规</strong>，HITL 处理那些<strong>需要人判断的"
            "灰色地带</strong>）与 L23 的可观测（人要<strong>看得到上下文 / trace</strong> 才能拍好这一板）。",
            "HITL lands in three common spots, all following one line — <strong>gate only where a gate belongs</strong>. "
            "<strong>(1) Approval gate</strong>: before an <strong>irreversible outward action</strong> (drop DB / "
            "transfer / order / mass-send), force a <strong>human yes/no</strong>, just like the <code>ApprovalFlow</code> "
            "above — execute on pass, abort otherwise. <strong>(2) Low-confidence fallback</strong>: when the model / "
            "retrieval is <strong>unsure</strong> (similarity too low, conflicting evidence, the model says “not sure”), "
            "<strong>don't fake it</strong> — escalate to a human; the key is a <strong>threshold</strong>: route to a "
            "human only <strong>below the line</strong>, answer high-confidence cases automatically, so HITL doesn't "
            "become “ask about everything”. <strong>(3) Confirm before sensitive tool calls</strong>: <strong>grade"
            "</strong> an agent's tools — mark <code>send_email</code> / <code>run_sql</code> / <code>place_order</code> "
            "as “sensitive” and pause for a human nod <strong>right before invoking them</strong>, while read-only / "
            "reversible tools (retrieval, weather) <strong>run on their own</strong>. All three solve the same problem: "
            "<strong>intercept the very few</strong> irreversible / high-risk / low-confidence points and hand them to a "
            "human, keeping the rest automatic — which dovetails with L25's guardrails (guardrails <strong>auto-block "
            "the obvious violations</strong>; HITL handles the <strong>gray zone that needs human judgment</strong>) and "
            "L23's observability (a human needs <strong>visible context / traces</strong> to make the call well).",
        ),
    )
    + c.analogy(L(
        "HITL 像网银<strong>支付前的“二次确认弹窗”</strong>：你平时查余额、看账单都<strong>畅通无阻</strong>，可一旦要"
        "<strong>真把钱转出去</strong>，屏幕就<strong>弹一个框</strong>——“确认向 ××× 转账 ¥5000？”——停在这里<strong>等你"
        "按下确认</strong>，你点了才扣款、取消就作罢。它<strong>不挡</strong>大多数操作，只在<strong>那一步不可逆的关键"
        "动作</strong>上拦一下，把最终决定权<strong>交回给你</strong>。",
        "HITL is like the <strong>“confirm” dialog before an online-banking payment</strong>: browsing your balance or "
        "statements flows <strong>freely</strong>, but the moment you actually <strong>move money out</strong>, a "
        "<strong>box pops up</strong> — “Confirm transferring ¥5000 to ×××?” — and it <strong>waits for you to press "
        "confirm</strong>; only then does it debit, and cancel calls it off. It <strong>blocks almost nothing</strong>, "
        "stepping in only at <strong>that one irreversible, critical action</strong>, handing the final decision "
        "<strong>back to you</strong>.",
    ))
    + c.key_points([
        L("HITL 是给<strong>不可逆 / 高风险动作</strong>（删库、转账、下单、外发）装的<strong>刹车</strong>：动手前暂停、"
          "等人确认——但<strong>只在该加闸的那一步加</strong>，不是每步都要人。",
          "HITL is a <strong>brake</strong> for <strong>irreversible / high-risk actions</strong> (drop DB, transfer, "
          "order, outbound): pause before acting and wait for a human — but <strong>gate only that step</strong>, not "
          "every step."),
        L("机制是一对事件的<strong>来回</strong>：一个 <code>@step</code> <strong>返回 <code>InputRequiredEvent</code>"
          "</strong>（自动写入事件流、挂起）；调用方<strong>流式取到</strong>后回一个 <code>HumanResponseEvent</code>，"
          "消费它的 <code>@step</code> 据 <code>response</code> 恢复 / 中止（<code>prefix</code> 带问题出去）。",
          "The mechanism is one <strong>round-trip</strong> of a pair of events: a <code>@step</code> <strong>returns "
          "<code>InputRequiredEvent</code></strong> (auto-written to the stream, pausing); the caller <strong>streams "
          "it</strong> and sends back a <code>HumanResponseEvent</code>, and the consuming <code>@step</code> resumes / "
          "aborts on <code>response</code> (<code>prefix</code> carries the question out)."),
        L("三个落点：<strong>审批闸</strong>（不可逆外部动作前）、<strong>低置信度兜底</strong>（分数过低 / 证据矛盾时转"
          "人）、<strong>敏感工具调用前确认</strong>（给工具分级，只对敏感的暂停）。",
          "Three landing spots: an <strong>approval gate</strong> (before irreversible external actions), a "
          "<strong>low-confidence fallback</strong> (escalate when scores are low / evidence conflicts), and "
          "<strong>confirming before sensitive tool calls</strong> (grade tools, pause only for sensitive ones)."),
        L("人是<strong>最贵的一层</strong>：每次确认都加延迟、打扰人——所以触发要<strong>省着用</strong>，并与 L25 护栏 + "
          "L23 trace <strong>叠成三层纵深</strong>（机器能判的别劳烦人，人判时要有上下文）。",
          "A human is the <strong>most expensive layer</strong>: each confirm adds latency and interruption — so trigger "
          "it <strong>sparingly</strong>, and stack it with L25 guardrails + L23 traces into <strong>three-layer "
          "defense in depth</strong> (don't bother a human with what a machine can judge; give context when a human does)."),
    ])
    + c.design_highlight(L(
        "人在回路的精髓，不是“让人盯着每一步”，而是<strong>把人放在最该放的那一个点上</strong>。L32 给了我们一支自由、"
        "能干的小队，可<strong>自由一旦延伸到不可逆的边界</strong>——删库、转账、外发——就危险了；HITL 就是那道"
        "<strong>刹车</strong>。但真正的设计判断<strong>不在“要不要人”，而在“在哪一步要人”</strong>：只在<strong>不可逆 / "
        "高风险 / 低置信</strong>的<strong>极少数</strong>点上暂停，其余全自动——闸加错地方，要么拦不住事故，要么把吞吐"
        "<strong>拖垮</strong>、把人<strong>烦走</strong>。把它放进全书的脉络看，这是<strong>三层纵深</strong>的最后一层："
        "<strong>L25 护栏</strong>自动挡掉<strong>明显违规</strong>（机器能判的，别劳烦人），<strong>L23 可观测</strong>把"
        "<strong>上下文 / trace</strong> 摆到人面前（让这一板拍得有依据），<strong>L33 HITL</strong> 在闸口让人做<strong>"
        "最后的拍板</strong>。人是<strong>最贵也最后</strong>的一层，所以只用在<strong>代价最高、最不可逆</strong>的地方。"
        "机制上它又轻得恰到好处：一个 <code>@step</code> 返回 <code>InputRequiredEvent</code> 就挂起、调用方回一个 "
        "<code>HumanResponseEvent</code> 就恢复——<strong>安全</strong>不是关掉自主，而是<strong>在关键一步把决定权短暂"
        "交回给人</strong>。下一课 <strong>L34</strong>，我们就把这套带着刹车的系统真正<strong>上线成服务</strong>。",
        "The essence of human-in-the-loop isn't “make a human watch every step” but <strong>placing the human at the "
        "one point that matters most</strong>. L32 handed us a free, capable team, but <strong>once that freedom "
        "reaches an irreversible boundary</strong> — dropping a DB, transferring money, sending outbound — it turns "
        "dangerous; HITL is that <strong>brake</strong>. Yet the real design call <strong>isn't “human or not” but “at "
        "which step”</strong>: pause only at the <strong>very few</strong> <strong>irreversible / high-risk / "
        "low-confidence</strong> points and keep the rest automatic — gate the wrong place and you either fail to stop "
        "the incident or <strong>grind throughput</strong> and <strong>annoy the human away</strong>. Seen across the "
        "whole book, this is the last of <strong>three layers of defense in depth</strong>: <strong>L25 guardrails</strong> "
        "auto-block the <strong>obvious violations</strong> (don't bother a human with what a machine can judge), "
        "<strong>L23 observability</strong> puts <strong>context / traces</strong> in front of the human (so the call is "
        "well-grounded), and <strong>L33 HITL</strong> lets a human make the <strong>final decision</strong> at the gate. "
        "The human is the <strong>most expensive, last</strong> layer, so spend it only where the downside is "
        "<strong>costliest and least reversible</strong>. And the mechanism stays just light enough: a <code>@step</code> "
        "returning <code>InputRequiredEvent</code> pauses, a caller's <code>HumanResponseEvent</code> resumes — "
        "<strong>safety</strong> isn't switching off autonomy but <strong>briefly handing the decision back to a human "
        "at the critical step</strong>. Next, <strong>L34</strong> takes this brake-equipped system and actually "
        "<strong>ships it as a service</strong>.",
    ))
)
LESSON_34 = (
    c.pipeline("answer")
    + c.lead(L(
        "前面 33 课，我们的 RAG 一直活在 <strong>notebook</strong> 里：建一次索引、问几个问题、看看效果——"
        "<strong>能跑一次就算赢</strong>。可真正交付时，它得变成一个 <strong>7×24 营业</strong>的<strong>服务</strong>："
        "通过 HTTP 同时接很多人的请求、要稳、要快。从原型到服务，<strong>最该避免的一件事</strong>就是——<strong>每来一个"
        "请求就重新加载 / 重建索引</strong>。建库（读文件、切块、embedding、写库）是<strong>一次性</strong>的重活，把它"
        "摊进<strong>每一次查询</strong>，结果就是又慢又浪费、并发一上来就垮。正解只有一句：<strong>索引在启动时一次"
        "加载、常驻内存，查询引擎复用</strong>，每个请求只跑「检索+合成」这段轻活。这一课就把这条规则落地："
        "① 用 <strong>FastAPI</strong> 把<strong>常驻的查询引擎</strong>包成一个 HTTP 接口，配 <strong>async "
        "<code>aquery</code> / 流式</strong>扛并发、降首 token 延迟（承 L24）；② 用 <strong>persist / "
        "<code>load_index_from_storage</code></strong> 让服务<strong>启动即秒级恢复</strong>、不必每次重建（承 L11）；"
        "③ 再往上，<strong>llama-deploy</strong> 编排多 workflow/服务、<strong>create-llama</strong> 脚手架快速起项目。"
        "<strong>说明：FastAPI / llama-deploy / create-llama 都在 core 之外，本课代码是示例</strong>；真正的 core 只有你"
        "早就会的 <code>StorageContext</code> / <code>load_index_from_storage</code> / <code>as_query_engine</code> / "
        "<code>aquery</code>。",
        "For 33 lessons our RAG has lived in a <strong>notebook</strong>: build the index once, ask a few questions, "
        "eyeball the result — <strong>running once is a win</strong>. But to actually ship it, it must become a "
        "<strong>24/7 service</strong>: taking many people's requests over HTTP at once, staying stable and fast. Going "
        "from prototype to service, the <strong>one thing to avoid most</strong> is <strong>reloading / rebuilding the "
        "index on every request</strong>. Building the library (read files, chunk, embed, write the store) is a "
        "<strong>one-time</strong> heavy job; smear it across <strong>every query</strong> and you get slow, wasteful "
        "work that collapses under concurrency. The fix is one sentence: <strong>load the index once at startup, keep it "
        "resident in memory, and reuse the query engine</strong>, so each request runs only the light “retrieve + "
        "synthesize” part. This lesson makes that rule concrete: (1) use <strong>FastAPI</strong> to wrap the "
        "<strong>resident query engine</strong> as an HTTP endpoint, with <strong>async <code>aquery</code> / "
        "streaming</strong> to handle concurrency and cut first-token latency (from L24); (2) use <strong>persist / "
        "<code>load_index_from_storage</code></strong> so the service <strong>restores in seconds at startup</strong> "
        "instead of rebuilding every time (from L11); (3) one level up, <strong>llama-deploy</strong> orchestrates "
        "multiple workflows/services and <strong>create-llama</strong> scaffolds a project fast. <strong>Note: FastAPI / "
        "llama-deploy / create-llama all live outside core; the code here is illustrative</strong>; the real core is "
        "only what you already know — <code>StorageContext</code> / <code>load_index_from_storage</code> / "
        "<code>as_query_engine</code> / <code>aquery</code>.",
    ))
    + d.compare2(
        (L("每请求重建索引", "Rebuild per request"), i18n.render(L(
            "每来一个请求就 <code>load</code> / 重建一次——把<strong>一次性建库成本</strong>摊进每次查询，又慢又浪费，"
            "并发一上来就垮。",
            "every request does a <code>load</code> / rebuild — smearing the <strong>one-time build cost</strong> into "
            "each query: slow, wasteful, and collapses under concurrency."))),
        (L("启动一次、引擎常驻", "Load once, engine resident"), i18n.render(L(
            "启动时<strong>一次加载</strong>索引、查询引擎<strong>常驻复用</strong>，每个请求只跑「检索+合成」——快、省、"
            "扛并发。",
            "load the index <strong>once</strong> at startup and <strong>reuse the resident</strong> query engine; each "
            "request runs only “retrieve + synthesize” — fast, cheap, concurrency-ready."))),
        caption=L("上线第一课：把建库成本留在启动，别摊进每次请求",
                  "Serving rule #1: keep the build cost at startup, don't smear it into every request"),
    )
    + c.section(
        L("① 从 notebook 到服务：索引一次加载常驻，别每请求重建",
          "① From notebook to service: load the index once and keep it resident — don't rebuild per request"),
        L(
            "<strong>notebook 和服务，活法完全不同</strong>。在 notebook 里，你<strong>从上往下跑一遍</strong>：建索引"
            "那个 cell 只执行<strong>一次</strong>，之后的 <code>query</code> 都复用内存里那个 index——<strong>跑通一次"
            "就够了</strong>。可服务是<strong>长命的、并发的</strong>：它常驻进程、通过 HTTP <strong>同时</strong>接很多"
            "请求，一天跑几万次。这时一个在 notebook 里<strong>看不出问题</strong>的写法会变成致命伤——<strong>把建索引"
            "写进请求处理函数里</strong>。建库是<strong>读文件 → 切块 → embedding → 写向量库</strong>这一整套重活，"
            "<strong>慢、烧钱、只需做一次</strong>；可一旦它躺在每个请求的代码路径上，就等于<strong>每问一个问题都把整个"
            "图书馆重建一遍</strong>——延迟高到没法用，embedding 费用成倍涨，并发稍一上来内存和算力就<strong>被重复建库"
            "吃垮</strong>。<strong>解法是把「建一次」和「查很多次」彻底分开</strong>：在<strong>服务启动时</strong>（模块"
            "加载 / app 启动）<strong>一次性</strong>把索引<strong>加载进内存</strong>，得到一个<strong>常驻的查询引擎"
            "</strong>；之后每个请求<strong>只调用这个已存在的引擎</strong>，跑「检索 + 合成」这段<strong>轻活</strong>。"
            "一句话——<strong>重活留在启动，请求里只剩轻活</strong>。这条规则贯穿后面三节：异步让「轻活」并发跑得更稳"
            "（②），持久化让「启动加载」便宜到秒级（③），编排让多个这样的服务协同（④）。",
            "<strong>A notebook and a service live completely differently.</strong> In a notebook you <strong>run top to "
            "bottom</strong>: the cell that builds the index runs <strong>once</strong>, and later <code>query</code> "
            "calls reuse that in-memory index — <strong>running it once is enough</strong>. A service is <strong>long-lived "
            "and concurrent</strong>: it sits resident in a process, takes many requests over HTTP <strong>at once</strong>, "
            "tens of thousands a day. Here a pattern that <strong>looks harmless in a notebook</strong> turns fatal — "
            "<strong>building the index inside the request handler</strong>. Building the library is the whole heavy chain "
            "of <strong>read files → chunk → embed → write the vector store</strong>: <strong>slow, costly, and needed "
            "only once</strong>; put it on every request's code path and you <strong>rebuild the entire library for every "
            "single question</strong> — latency too high to use, embedding bills multiplying, and memory/compute "
            "<strong>crushed by repeated rebuilds</strong> the moment concurrency rises. <strong>The fix is to fully "
            "separate “build once” from “query many times”</strong>: at <strong>service startup</strong> (module load / "
            "app startup) load the index into memory <strong>once</strong>, yielding a <strong>resident query "
            "engine</strong>; then each request <strong>calls that already-existing engine</strong> to run the "
            "<strong>light</strong> “retrieve + synthesize” part. In a line — <strong>keep the heavy work at startup, "
            "leave only light work in the request</strong>. This rule runs through the next three sections: async makes "
            "the “light work” run concurrently and stably (②), persistence makes “startup loading” cheap down to seconds "
            "(③), and orchestration lets many such services cooperate (④).",
        ),
    )
    + c.code(
        "# pip install fastapi uvicorn  —— 以下为示例，FastAPI/llama-deploy 在 core 之外\n"
        "from fastapi import FastAPI\n"
        "from llama_index.core import StorageContext, load_index_from_storage\n\n"
        "app = FastAPI()\n"
        "index = load_index_from_storage(StorageContext.from_defaults(persist_dir=\"./store\"))  # 启动时一次加载\n"
        "qe = index.as_query_engine()\n\n"
        "@app.post(\"/query\")\n"
        "async def query(q: str):\n"
        "    return {\"answer\": str(await qe.aquery(q))}   # 异步，承 L24",
        caption=L("示例服务：模块级一次 load_index_from_storage 常驻、引擎复用；请求里只 await aquery（FastAPI 在 core 之外）",
                  "Illustrative service: module-level load_index_from_storage once and resident, engine reused; the request only awaits aquery (FastAPI is outside core)"),
    )
    + c.source_ref(
        "indices/loading.py", "load_index_from_storage",
        L("从磁盘恢复已建好的索引，服务启动时一次加载常驻。",
          "restores a persisted index from disk — loaded once at service startup."),
    )
    + d.layers([
        (L("HTTP 请求", "HTTP request"), L("FastAPI 路由", "FastAPI route")),
        (L("常驻查询引擎", "long-lived query engine"), L("启动时一次加载索引", "index loaded once at boot")),
        (L("检索 + 合成", "retrieve + synthesize"), L("异步/流式", "async/streaming")),
        (L("LLM", "LLM"), L("生成答案", "generates answer")),
    ], caption=L("上线关键：索引常驻、查询引擎复用，别每请求重建",
                 "serving rule: keep the index resident and reuse the engine — don't rebuild per request"))
    + c.section(
        L("② 用 FastAPI 把查询引擎包成接口：async <code>aquery</code> / 流式扛并发（承 L24）",
          "② Wrap the query engine as an endpoint with FastAPI: async <code>aquery</code> / streaming for concurrency (from L24)"),
        L(
            "有了常驻的查询引擎，<strong>剩下的只是「把它接到网上」</strong>。<strong>FastAPI</strong>（"
            "<code>pip install fastapi uvicorn</code>，<strong>core 之外</strong>的 Web 框架，本课只作示例）正合适："
            "它<strong>原生 async</strong>，和我们 L24 学的 <code>aquery</code> <strong>天生一对</strong>。为什么要 "
            "async？因为 RAG 的一次查询，大半时间<strong>卡在等 LLM / 等向量库返回</strong>——这是 <strong>I/O 等待"
            "</strong>，不是 CPU 在算。同步的 <code>query</code> 会<strong>把整个进程堵死</strong>在这一次等待上，后面"
            "排队的请求只能干等；而 <code>async def</code> + <code>await qe.aquery(q)</code> 在等待时<strong>把控制权"
            "交还事件循环</strong>，让<strong>别的请求继续跑</strong>——同样一台机器，并发吞吐立刻上一个台阶（承 L24 的"
            "「异步/批」）。另一半是<strong>体验</strong>：用<strong>流式</strong>（承 L24）让答案<strong>逐 token 边生成"
            "边吐</strong>，用户几百毫秒就看到第一个字，而不是干等整段生成完——<strong>首 token 延迟</strong>骤降，总"
            "时长几乎不变。要记牢 L24 的那句话：<strong>流式优化的是「首字延迟」与体验，不是总耗时</strong>。<strong>"
            "分清边界</strong>：<code>aquery</code> 是<strong>core 的真方法</strong>（它能直接收一个字符串问题）；"
            "<code>FastAPI</code> / <code>uvicorn</code> 是<strong>外部工具</strong>，只是把这个 core 能力<strong>暴露成 "
            "HTTP</strong>。",
            "With a resident query engine, <strong>all that's left is “wiring it to the network”.</strong> "
            "<strong>FastAPI</strong> (<code>pip install fastapi uvicorn</code>, a Web framework <strong>outside "
            "core</strong>, illustrative here) fits well: it is <strong>natively async</strong> and a <strong>natural "
            "match</strong> for the <code>aquery</code> we learned in L24. Why async? Because most of a RAG query's time "
            "is <strong>spent waiting on the LLM / the vector store</strong> — that's <strong>I/O wait</strong>, not CPU "
            "work. A synchronous <code>query</code> <strong>blocks the whole process</strong> on that one wait, so queued "
            "requests just sit idle; whereas <code>async def</code> + <code>await qe.aquery(q)</code> <strong>yields "
            "control back to the event loop</strong> while waiting, letting <strong>other requests keep running</strong> "
            "— on the same machine, concurrent throughput jumps a level (L24's “async / batch”). The other half is "
            "<strong>experience</strong>: <strong>streaming</strong> (from L24) emits the answer <strong>token by token "
            "as it generates</strong>, so the user sees the first character in a few hundred milliseconds instead of "
            "waiting for the whole thing — <strong>first-token latency</strong> drops sharply while total time barely "
            "changes. Remember L24's line: <strong>streaming optimizes “first-token latency” and experience, not total "
            "time</strong>. <strong>Keep the boundary clear</strong>: <code>aquery</code> is a <strong>real core "
            "method</strong> (it takes a string question directly); <code>FastAPI</code> / <code>uvicorn</code> are "
            "<strong>external tools</strong> that merely <strong>expose</strong> that core capability <strong>over "
            "HTTP</strong>.",
        ),
    )
    + c.section(
        L("③ 持久化：<code>persist</code> / <code>load_index_from_storage</code> 让启动即秒级恢复（承 L11）",
          "③ Persistence: <code>persist</code> / <code>load_index_from_storage</code> for second-level startup recovery (from L11)"),
        L(
            "「启动时一次加载」要真便宜，<strong>前提是别在启动时也重建一遍</strong>。如果每次服务启动都从原始文档"
            "<strong>重新切块、重新 embedding</strong>，那「建库的重活」只是从「每请求」挪到了「每次重启 / 每次扩容」"
            "——<strong>部署一次等几分钟、还白烧 embedding 钱</strong>。L11 的<strong>持久化</strong>正是为此：<strong>"
            "建一次、落一次盘</strong>——<code>index.storage_context.persist(persist_dir=\"./store\")</code> 把 docstore / "
            "index / 向量整套写到磁盘；之后服务启动只需 <code>load_index_from_storage(StorageContext.from_defaults("
            "persist_dir=\"./store\"))</code>，<strong>秒级</strong>把索引读回内存，<strong>免去重建</strong>。这正是上面 "
            "code① 启动那一行在做的事。这两个符号都是<strong>实打实的 core</strong>（<code>StorageContext</code> 来自 "
            "<code>storage_context.py</code>、<code>load_index_from_storage</code> 来自 <code>indices/loading.py</code>），"
            "不依赖任何外部框架。<strong>再往规模化看一步</strong>：当你跑<strong>多个副本</strong>（多进程 / 多机水平"
            "扩展）时，别让每个副本各存一份本地索引，而是让它们<strong>共享同一份持久化存储</strong>，或干脆把向量接到"
            "<strong>外置向量库</strong>（L09 学过的 Chroma / pgvector / Qdrant…）——这样「加载一次」对每个副本都成立，"
            "数据也只有一处真相。",
            "For “load once at startup” to be truly cheap, <strong>you must not rebuild at startup either</strong>. If "
            "every service start <strong>re-chunks and re-embeds</strong> from the raw documents, the “build heavy "
            "lifting” has merely moved from “per request” to “per restart / per scale-out” — <strong>minutes of wait per "
            "deploy and wasted embedding spend</strong>. L11's <strong>persistence</strong> exists for this: "
            "<strong>build once, write once</strong> — <code>index.storage_context.persist(persist_dir=\"./store\")</code> "
            "writes the docstore / index / vectors to disk; afterward a service start only needs "
            "<code>load_index_from_storage(StorageContext.from_defaults(persist_dir=\"./store\"))</code> to read the index "
            "back into memory in <strong>seconds</strong>, <strong>skipping the rebuild</strong>. This is exactly what "
            "the startup line in code① above does. Both symbols are <strong>genuine core</strong> "
            "(<code>StorageContext</code> from <code>storage_context.py</code>, <code>load_index_from_storage</code> from "
            "<code>indices/loading.py</code>), depending on no external framework. <strong>One step toward scale</strong>: "
            "when you run <strong>multiple replicas</strong> (multi-process / multi-machine horizontal scaling), don't let "
            "each replica keep its own local copy — have them <strong>share one persisted store</strong>, or connect "
            "vectors to an <strong>external vector DB</strong> (the Chroma / pgvector / Qdrant… from L09) — so “load "
            "once” holds for every replica and the data has a single source of truth.",
        ),
    )
    + c.section(
        L("④ 更进一步：<code>llama-deploy</code> 编排多 workflow/服务、<code>create-llama</code> 脚手架起项目",
          "④ Going further: <code>llama-deploy</code> orchestrates multi-workflow services, <code>create-llama</code> scaffolds a project"),
        L(
            "一个 FastAPI 文件足够把<strong>单个</strong>查询引擎送上线；但当系统长大——L32 的<strong>多 agent / 多 "
            "workflow</strong>、L33 的 <strong>HITL 审批</strong>都要协同时，你会想要<strong>编排</strong>而不是手搓。"
            "这里有两件 <strong>core 之外</strong>的官方工具（同样只作示例）：<strong>① <code>llama-deploy</code></strong>"
            "——把你写好的 <strong>workflow 部署成可独立伸缩、能互相通信的网络服务</strong>，多个 workflow/服务由它统一"
            "编排、扩缩容，等于把 L26–L33 搭的那套<strong>从「一个进程里的对象」升级成「一组分布式服务」</strong>。"
            "<strong>② <code>create-llama</code></strong>——一个<strong>脚手架 CLI</strong>（<code>npx create-llama"
            "</code>），一条命令生成<strong>前端 + 后端 + 数据摄取</strong>的全栈起手项目，省去你手搓 API、UI、ingestion "
            "的样板，<strong>几分钟就能跑起一个能问答的网站</strong>。<strong>务必记住边界</strong>：<code>llama-deploy"
            "</code> / <code>create-llama</code> / <code>FastAPI</code> 都<strong>不是 core</strong>，它们是<strong>打包"
            "与编排</strong>层；真正干活的<strong>核心始终没变</strong>——还是你早已会的<strong>索引、查询引擎、workflow"
            "</strong>。<strong>怎么选</strong>：起步 / 单服务，<strong>FastAPI 足矣</strong>；要从零快速起一个全栈项目，"
            "用 <strong>create-llama</strong> 脚手架；要把多个 workflow/服务编排成分布式系统，再上 <strong>llama-deploy"
            "</strong>。",
            "A single FastAPI file is enough to ship <strong>one</strong> query engine; but as the system grows — L32's "
            "<strong>multi-agent / multi-workflow</strong> and L33's <strong>HITL approvals</strong> all need to cooperate "
            "— you'll want <strong>orchestration</strong> rather than hand-wiring. Here are two <strong>out-of-core</strong> "
            "official tools (again illustrative only): <strong>(1) <code>llama-deploy</code></strong> — deploys the "
            "workflows you wrote as <strong>independently scalable, mutually communicating networked services</strong>, "
            "orchestrating and autoscaling many workflows/services, effectively upgrading the L26–L33 stack <strong>from "
            "“objects in one process” to “a set of distributed services”</strong>. <strong>(2) <code>create-llama</code>"
            "</strong> — a <strong>scaffold CLI</strong> (<code>npx create-llama</code>) that generates a full-stack "
            "starter with <strong>frontend + backend + ingestion</strong> in one command, sparing you the boilerplate of "
            "hand-building API, UI, and ingestion, so <strong>a working Q&amp;A site runs in minutes</strong>. "
            "<strong>Keep the boundary firmly in mind</strong>: <code>llama-deploy</code> / <code>create-llama</code> / "
            "<code>FastAPI</code> are <strong>not core</strong> — they are a <strong>packaging and orchestration</strong> "
            "layer; the <strong>core that does the real work never changed</strong> — still the <strong>index, query "
            "engine, and workflow</strong> you already know. <strong>How to choose</strong>: for a start / single service, "
            "<strong>FastAPI is enough</strong>; to spin up a full-stack project from scratch fast, use the "
            "<strong>create-llama</strong> scaffold; to orchestrate many workflows/services into a distributed system, "
            "reach for <strong>llama-deploy</strong>.",
        ),
    )
    + d.flow([
        ("nb", L("notebook 原型", "notebook prototype")),
        ("api", L("FastAPI 服务", "FastAPI service"), L("并发/流式", "concurrent/streaming")),
        ("deploy", L("llama-deploy / create-llama", "llama-deploy / create-llama"), L("编排/脚手架", "orchestration/scaffold")),
    ], caption=L("从原型到生产服务的进阶路径", "the path from prototype to a production service"))
    + c.analogy(L(
        "把 RAG 上线，就像把<strong>实验台上的原型</strong>搬进一家<strong>7×24 营业的店面</strong>。在实验台上，原型"
        "<strong>能点亮一次</strong>就算成功——你亲手接线、跑一遍、记下结果。可开门做生意完全是另一回事：店面要"
        "<strong>常年不打烊</strong>、要<strong>同时接待很多客人</strong>、上菜要<strong>快</strong>。于是你不会"
        "<strong>每来一位客人就重盖一次厨房</strong>（那就是「每请求重建索引」）——厨房<strong>开业前就装好、一直"
        "备着</strong>（索引常驻），客人来了只管<strong>下单上菜</strong>（检索+合成）；还得能<strong>同时招呼多桌"
        "</strong>（async 并发）、先<strong>端上一道前菜</strong>稳住客人（流式降首字延迟）；打烊重开也不必重装厨房"
        "（持久化）。原型只要<strong>能跑一次</strong>，店面要<strong>稳、要快、要能同时接客</strong>——这一步之差，"
        "就是 notebook 与服务的全部距离。",
        "Shipping a RAG is like moving a <strong>prototype off the lab bench</strong> into a <strong>shop open "
        "24/7</strong>. On the bench, lighting the prototype <strong>up once</strong> is success — you wire it by hand, "
        "run it through, note the result. Opening for business is another matter entirely: the shop must <strong>never "
        "close</strong>, <strong>serve many customers at once</strong>, and bring food out <strong>fast</strong>. So you "
        "don't <strong>rebuild the kitchen for every customer who walks in</strong> (that's “rebuild the index per "
        "request”) — the kitchen is <strong>installed before opening and kept ready</strong> (a resident index), and "
        "each guest just <strong>orders and is served</strong> (retrieve + synthesize); you also <strong>wait many "
        "tables at once</strong> (async concurrency) and <strong>bring out a starter first</strong> to settle them "
        "(streaming cuts first-token latency); closing and reopening needn't reinstall the kitchen (persistence). A "
        "prototype only has to <strong>run once</strong>; a shop has to be <strong>stable, fast, and able to serve many "
        "at once</strong> — that gap is the whole distance between a notebook and a service.",
    ))
    + c.key_points([
        L("<strong>索引常驻、引擎复用，别每请求重建</strong>：建库（读文件 / 切块 / embedding / 写库）是一次性重活，"
          "摊进每次查询就又慢又浪费——启动时一次 <code>load_index_from_storage</code> 加载、查询引擎常驻，请求里只跑"
          "「检索+合成」。",
          "<strong>Keep the index resident, reuse the engine, don't rebuild per request</strong>: building the library "
          "(read files / chunk / embed / write) is one-time heavy work, and smearing it across every query is slow and "
          "wasteful — load once at startup with <code>load_index_from_storage</code>, keep the query engine resident, "
          "and run only “retrieve + synthesize” in the request."),
        L("<strong>FastAPI 只是示例 Web 框架（core 之外）</strong>：用 <code>async def</code> + "
          "<code>await qe.aquery(q)</code> 扛并发、用流式降首 token 延迟（都承 L24）；真正的 core 是<strong>查询引擎与 "
          "<code>aquery</code></strong>，FastAPI 只是把它暴露成 HTTP。",
          "<strong>FastAPI is just an illustrative Web framework (outside core)</strong>: use <code>async def</code> + "
          "<code>await qe.aquery(q)</code> for concurrency and streaming to cut first-token latency (both from L24); the "
          "real core is the <strong>query engine and <code>aquery</code></strong>, FastAPI only exposes it over HTTP."),
        L("<strong>持久化让「启动即恢复」便宜</strong>：<code>persist</code> 落盘、<code>load_index_from_storage</code> "
          "秒级读回（承 L11），别在每次重启 / 扩容时重建；多副本应<strong>共享同一存储 / 外置向量库</strong>。",
          "<strong>Persistence makes “restore at startup” cheap</strong>: <code>persist</code> to disk and "
          "<code>load_index_from_storage</code> back in seconds (from L11), don't rebuild on every restart / scale-out; "
          "replicas should <strong>share one store / an external vector DB</strong>."),
        L("<strong>再进一步是编排，不是新核心</strong>：<code>llama-deploy</code> 把多 workflow/服务编排成分布式系统、"
          "<code>create-llama</code> 脚手架快速起全栈项目——都在 core 之外、代码为示例。",
          "<strong>The next step is orchestration, not a new core</strong>: <code>llama-deploy</code> orchestrates "
          "multi-workflow services into a distributed system, <code>create-llama</code> scaffolds a full-stack project "
          "fast — both outside core, illustrative code."),
        L("<strong>分清 core 与外部工具</strong>：<code>StorageContext</code> / <code>load_index_from_storage</code> / "
          "<code>as_query_engine</code> / <code>aquery</code> 是 core；<code>FastAPI</code> / <code>llama-deploy</code> / "
          "<code>create-llama</code> 是外部工具，按需取用、别当核心内置。",
          "<strong>Tell core from external tools</strong>: <code>StorageContext</code> / "
          "<code>load_index_from_storage</code> / <code>as_query_engine</code> / <code>aquery</code> are core; "
          "<code>FastAPI</code> / <code>llama-deploy</code> / <code>create-llama</code> are external tools — use on "
          "demand, don't mistake them for core built-ins."),
    ])
    + c.design_highlight(L(
        "上线这一课，<strong>几乎没有新的 RAG 概念</strong>——它的全部重量压在一句运维直觉上：<strong>把一次性的重活"
        "留在启动，把高频的轻活留在请求</strong>。<strong>索引常驻、查询引擎复用，别每请求重建</strong>——这就是 "
        "notebook 与服务之间唯一却致命的那道坎。想清楚这一点，剩下的拼图你<strong>早就备齐了</strong>：L24 的 "
        "<strong>async <code>aquery</code> + 流式</strong>解决「同时接客」与「首字延迟」，L11 的 <strong>persist / "
        "load</strong> 让「启动即恢复」便宜到秒级；FastAPI 只是把这套 core 能力<strong>接到网上</strong>的一层皮，"
        "llama-deploy / create-llama 则在更高处<strong>编排与脚手架</strong>——它们都在 core 之外，核心始终是你<strong>"
        "从第 1 课搭到第 33 课</strong>的那条 RAG 管线。而「上线」从来不是终点：服务跑起来之后，质量靠全书攒下的那套"
        "<strong>纵深</strong>持续兜住——<strong>L22 回归闸</strong>在每次发布前挡住退化，<strong>L23 trace</strong> 在"
        "出错时定位是检索还漏在生成，<strong>L25 护栏</strong>自动挡掉明显违规，必要时再用 <strong>L33 HITL</strong> 在"
        "不可逆的关口让人拍板。一句话收束：<strong>上线不是写新魔法，而是把你已经会的东西，按「常驻 + 异步 + 持久化」"
        "的纪律稳稳地摆上货架</strong>。",
        "This shipping lesson brings <strong>almost no new RAG concept</strong> — its whole weight rests on one ops "
        "instinct: <strong>keep the one-time heavy work at startup and the high-frequency light work in the "
        "request</strong>. <strong>Keep the index resident, reuse the query engine, don't rebuild per request</strong> — "
        "that is the single, fatal step between a notebook and a service. Get that, and the rest of the puzzle you "
        "<strong>already have</strong>: L24's <strong>async <code>aquery</code> + streaming</strong> handles “serving "
        "many at once” and “first-token latency”, and L11's <strong>persist / load</strong> makes “restore at startup” "
        "cheap down to seconds; FastAPI is just a skin that <strong>wires this core capability to the network</strong>, "
        "while llama-deploy / create-llama <strong>orchestrate and scaffold</strong> one level up — all outside core, "
        "the core still being the RAG pipeline you <strong>built from L1 through L33</strong>. And “going live” is never "
        "the finish line: once the service runs, quality is held up by the <strong>defense in depth</strong> the whole "
        "book accumulated — <strong>L22's regression gate</strong> blocks regressions before each release, <strong>L23's "
        "traces</strong> localize whether a miss was in retrieval or generation, <strong>L25's guardrails</strong> "
        "auto-block obvious violations, and <strong>L33's HITL</strong> hands the call to a human at irreversible gates "
        "when needed. To close in a line: <strong>shipping isn't writing new magic — it's placing what you already know "
        "on the shelf, steadily, under the discipline of “resident + async + persistent”</strong>.",
    ))
)
LESSON_35 = (
    c.pipeline("embed")
    + c.lead(L(
        "走到全书<strong>最后一课</strong>，RAG 的每个零件你都见过了——可有一个最底层的零件，我们从头到尾"
        "<strong>原样拿来用</strong>：<strong>embedding 模型</strong>。它把文字映射成向量、决定“谁和谁相近”，是检索的"
        "<strong>地基</strong>。通用 embedding（<code>bge</code> / <code>text-embedding-3</code> 之类）在<strong>大众语料"
        "</strong>上训练，泛泛场景够用；可一旦进了<strong>专业领域</strong>——医疗、法律、芯片、你公司内部的黑话——它常常"
        "<strong>语义错位</strong>：把<strong>专业术语 / 缩写 / 内部简称</strong>映射得不准，本该相近的概念在向量空间里"
        "<strong>离得老远</strong>，于是<strong>召回不到位</strong>，后面 rerank、合成做得再好也救不回来。这一课讲<strong>最后"
        "一招</strong>：用<strong>自家文档</strong>自动造 <strong>(问题, 相关块)</strong> 训练对、<strong>微调 embedding"
        "</strong>，把领域语义<strong>校准</strong>进向量空间——正样本拉近、负样本推远。但要<strong>先把两件事说在前头"
        "</strong>：① <strong>微调成本高、易过拟合</strong>，它该是<strong>穷尽更便宜手段之后</strong>的最后一步，不是第一"
        "反应；② <strong>llama-index-finetuning 在 core 之外</strong>（<code>pip install llama-index-finetuning</code>），"
        "本课代码是<strong>示例</strong>，重点在<strong>思路与判断</strong>，不在 API 细节。",
        "At the book's <strong>final lesson</strong>, you've met every part of RAG — yet one foundational part we kept "
        "<strong>using as-is</strong> from start to finish: the <strong>embedding model</strong>. It maps text to "
        "vectors and decides “who is near whom” — the <strong>bedrock</strong> of retrieval. Generic embeddings "
        "(<code>bge</code> / <code>text-embedding-3</code> and friends) are trained on <strong>broad corpora</strong> "
        "and serve general cases well; but step into a <strong>specialized domain</strong> — medicine, law, chips, your "
        "company's internal slang — and they often <strong>misalign</strong>: mapping <strong>jargon / acronyms / "
        "internal shorthand</strong> imprecisely, so concepts that should be near sit <strong>far apart</strong> in "
        "vector space, retrieval <strong>under-recalls</strong>, and no amount of downstream rerank or synthesis can "
        "recover it. This lesson covers the <strong>last resort</strong>: use <strong>your own documents</strong> to "
        "auto-build <strong>(question, relevant-chunk)</strong> training pairs and <strong>fine-tune the embedding"
        "</strong>, calibrating domain semantics into the vector space — pulling positives closer and pushing negatives "
        "apart. But <strong>two caveats first</strong>: (1) fine-tuning is <strong>costly and overfits easily</strong>, "
        "so it should be the <strong>last step after exhausting cheaper means</strong>, not the first reflex; (2) "
        "<strong>llama-index-finetuning lives outside core</strong> (<code>pip install llama-index-finetuning</code>), "
        "and the code here is <strong>illustrative</strong> — the point is the <strong>reasoning and judgment</strong>, "
        "not API details.",
    ))
    + d.compare2(
        (L("通用 embedding", "Generic embedding"),
         i18n.render(L("领域术语<strong>语义错位</strong>，相关块排不上来", "domain terms <strong>misalign</strong>; relevant chunks rank low"))),
        (L("领域微调后", "After fine-tuning"),
         i18n.render(L("正样本拉近、负样本推远 → 召回更准", "positives pulled closer, negatives pushed apart → better recall"))),
        caption=L("微调把你的领域语义“校准”进向量空间", "fine-tuning calibrates your domain semantics into the vector space"),
    )
    + c.section(
        L("① 痛点：通用 embedding 在专业领域“语义错位”，召回从地基就漏",
          "① The pain: generic embeddings “misalign” in a specialized domain — retrieval leaks from the foundation"),
        L(
            "<strong>embedding 是检索的地基</strong>：它决定每段文字落在向量空间的哪个位置，而 top-k 召回<strong>只看谁离"
            "查询近</strong>。通用 embedding 在<strong>大众语料</strong>上训练，专业领域的词在它眼里要么<strong>稀薄</strong>、"
            "要么<strong>歧义</strong>。举两个例子：缩写 <strong>“MI”</strong> 在通用语料里更像 Michigan 或 Mutual "
            "Information，可在心内科它是<strong>“心肌梗死”</strong>；你公司内部的<strong>项目代号、产品简称、黑话</strong>，"
            "通用模型<strong>压根没见过</strong>。结果是：用户拿<strong>领域术语</strong>去问，真正相关的块因为<strong>向量不"
            "相近</strong>而<strong>排不进 top-k</strong>——召回阶段就把答案漏在了门外。这条漏一旦发生，<strong>后面救不回</strong>："
            "L21 的 rerank 只能在<strong>已召回的候选</strong>里重排，<strong>召回时就没捞上来的块，rerank 给不出来</strong>；"
            "合成器再聪明，也只能拿手里这几个错块去拼。所以当你用 L23 的 trace + <strong>L12</strong> 的检索指标（hit-rate / MRR）确认<strong>错就错在“检索召回”"
            "</strong>、且根因是<strong>领域语义错位</strong>时，才轮到微调——它修的正是这层最底下的地基。",
            "<strong>The embedding is retrieval's foundation</strong>: it fixes where each piece of text lands in vector "
            "space, and top-k recall <strong>only looks at what's nearest the query</strong>. Generic embeddings train "
            "on <strong>broad corpora</strong>, where domain words are either <strong>thin</strong> or "
            "<strong>ambiguous</strong>. Two examples: the acronym <strong>“MI”</strong> in general text reads as "
            "Michigan or Mutual Information, but in cardiology it means <strong>“myocardial infarction”</strong>; your "
            "company's <strong>project codenames, product nicknames, and slang</strong> the generic model has "
            "<strong>simply never seen</strong>. The result: a user asks with <strong>domain terms</strong>, and the "
            "truly relevant chunk — because its vector <strong>isn't near</strong> — <strong>never enters the top-k</strong>, "
            "so retrieval leaves the answer outside the door. Once that leak happens, <strong>nothing downstream "
            "recovers it</strong>: L21's rerank can only reorder <strong>already-retrieved candidates</strong>, and "
            "<strong>a chunk never recalled can't be re-ranked into existence</strong>; however clever the synthesizer, "
            "it can only stitch from the wrong chunks it holds. So only when L23's traces + <strong>L12</strong>'s retrieval metrics (hit-rate / MRR) confirm the "
            "fault is <strong>in “retrieval recall”</strong> and the root cause is <strong>domain misalignment</strong> "
            "does fine-tuning's turn arrive — it repairs exactly that deepest foundation.",
        ),
    )
    + c.section(
        L("② 思路：用自家 QA 对当“信号”，把正样本拉近、负样本推远",
          "② The idea: use your own QA pairs as the “signal” — pull positives closer, push negatives apart"),
        L(
            "微调 embedding 的本质是<strong>对比学习</strong>：喂给模型一批“<strong>这条问题</strong>和<strong>这个块</strong>"
            "是相关的（正样本）”的例子，让它微调权重，<strong>把相关的问题与块在向量空间里拉近</strong>，同时<strong>把不相关"
            "的推远</strong>。难点只有一个：<strong>哪来这么多标注好的 (问题, 相关块) 对</strong>？答案很巧——<strong>用你自家"
            "的文档自动造</strong>。把文档切成块（你早在 L06 就会），对<strong>每个块</strong>让一个 LLM <strong>反向生成</strong>"
            "“这个块能回答的问题”——于是 (生成的问题, 这个块) 天然是一对<strong>正样本</strong>，同一批里的其它块自然充当"
            "<strong>负样本</strong>。这正是 <code>generate_qa_embedding_pairs(nodes, llm=...)</code> 做的事：喂进 nodes，吐"
            "出一个<strong>可直接用于微调的 embedding QA 数据集</strong>。要清醒的是：这些问题是<strong>机器造的</strong>，质量"
            "参差，应当<strong>自动生成打底 + 人工抽检过滤 + 补难负样本</strong>（详见本课面试题）——<strong>数据质量直接决定"
            "微调的上限</strong>，“垃圾进”只会“垃圾出”。",
            "Fine-tuning an embedding is at heart <strong>contrastive learning</strong>: feed the model a batch of “<strong>"
            "this question</strong> and <strong>this chunk</strong> are relevant (a positive)” examples and let it nudge "
            "its weights to <strong>pull related questions and chunks closer</strong> in vector space while <strong>pushing "
            "unrelated ones apart</strong>. There's only one hard part: <strong>where do all those labeled (question, "
            "relevant-chunk) pairs come from</strong>? The neat answer — <strong>auto-build them from your own "
            "documents</strong>. Chunk the docs (you've done this since L06), and for <strong>each chunk</strong> have an "
            "LLM <strong>reverse-generate</strong> “a question this chunk can answer” — so (generated question, this "
            "chunk) is naturally a <strong>positive</strong>, and the other chunks in the batch serve as "
            "<strong>negatives</strong>. That is exactly what <code>generate_qa_embedding_pairs(nodes, llm=...)</code> "
            "does: feed in nodes, get back an <strong>embedding QA dataset ready for fine-tuning</strong>. Stay "
            "clear-eyed: these questions are <strong>machine-made</strong> and uneven, so you should <strong>auto-generate "
            "as a base + human spot-check to filter + add hard negatives</strong> (see this lesson's interview drills) — "
            "<strong>data quality sets the ceiling of fine-tuning</strong>, and “garbage in” only yields “garbage out”.",
        ),
    )
    + c.section(
        L("③ 流程：造对 → 微调 → 换模型重建索引 → 用 L19/L22 量化提升",
          "③ The flow: build pairs → fine-tune → rebuild the index with the new model → quantify the gain via L19/L22"),
        L(
            "整条链是一个<strong>四步闭环</strong>，每一步都有 <strong>llama-index-finetuning（core 之外，示例）</strong>的对应"
            "符号。① <strong>造对</strong>：<code>generate_qa_embedding_pairs(nodes, llm=...)</code> 自动产出 QA 数据集（见 ②）。"
            "② <strong>微调</strong>：<code>SentenceTransformersFinetuneEngine(dataset, model_id=基座, model_output_path=...)"
            "</code> 在你的 QA 对上<strong>接着训练</strong>一个开源 sentence-transformer（如 <code>bge-small</code>），"
            "<code>.finetune()</code> 跑完、<code>get_finetuned_model()</code> 取回一个<strong>领域版</strong> embedding。"
            "③ <strong>换模型重建索引</strong>——<strong>最容易被忽略、却必须做</strong>的一步：embedding 一旦换了，<strong>旧"
            "索引里的向量是旧模型算的、不能和新模型混用</strong>，必须把微调模型设成 <code>Settings.embed_model</code>、"
            "<strong>重新 embedding 整库、重建索引</strong>（这也提醒你微调有多贵——要重跑一遍建库）。④ <strong>量化提升"
            "</strong>——<strong>最不能省</strong>的一步：微调到底有没有用、有没有过拟合，<strong>必须用数字证明</strong>。用 "
            "<strong>L12</strong> 的检索指标（<strong>hit-rate / MRR</strong>）——以 <code>RetrieverEvaluator</code> 在一组"
            "<strong>留出的</strong>测试问题上算——按 <strong>L19/L22</strong> 的“用数字证明、并入回归”纪律对比微调<strong>前后"
            "</strong>；再承 L22 把它固化成<strong>回归集</strong>，确保这次微调没在别的查询类型上<strong>悄悄带崩</strong>。"
            "<strong>只看训练 loss 下降是自欺</strong>——loss 降只说明模型记住了这批 QA 对，既不等于检索更准，更可能是过拟合"
            "的信号。",
            "The whole chain is a <strong>four-step loop</strong>, each step with a symbol from <strong>llama-index-finetuning "
            "(outside core, illustrative)</strong>. (1) <strong>Build pairs</strong>: "
            "<code>generate_qa_embedding_pairs(nodes, llm=...)</code> auto-produces the QA dataset (see (2)). (2) "
            "<strong>Fine-tune</strong>: <code>SentenceTransformersFinetuneEngine(dataset, model_id=base, "
            "model_output_path=...)</code> <strong>continues training</strong> an open-source sentence-transformer (e.g. "
            "<code>bge-small</code>) on your QA pairs; <code>.finetune()</code> runs and "
            "<code>get_finetuned_model()</code> returns a <strong>domain version</strong> of the embedding. (3) "
            "<strong>Rebuild the index with the new model</strong> — the <strong>easily-missed but mandatory</strong> "
            "step: once the embedding changes, <strong>the old index's vectors were computed by the old model and "
            "can't be mixed with the new one</strong>, so you must set the fine-tuned model as "
            "<code>Settings.embed_model</code> and <strong>re-embed the whole corpus and rebuild the index</strong> (a "
            "reminder of how costly fine-tuning is — you re-run the build). (4) <strong>Quantify the gain</strong> — the "
            "<strong>step you must not skip</strong>: whether fine-tuning actually helped or overfit <strong>must be "
            "proven with numbers</strong>. Compute the <strong>L12</strong> retrieval metrics (<strong>hit-rate / MRR"
            "</strong>) with <code>RetrieverEvaluator</code> on a <strong>held-out</strong> set, following "
            "<strong>L19/L22</strong>'s prove-with-numbers + regression discipline, and compare <strong>before vs "
            "after</strong>; per L22, freeze it into a <strong>regression set</strong> so this fine-tune didn't "
            "<strong>quietly tank</strong> other query types. <strong>Watching only the training loss drop is "
            "self-deception</strong> — a falling loss just means the model memorized these QA pairs, which is "
            "not sharper retrieval, and more likely a sign of overfitting.",
        ),
    )
    + c.code(
        "# pip install llama-index-finetuning  —— 示例，微调在 core 之外\n"
        "from llama_index.finetuning import generate_qa_embedding_pairs, SentenceTransformersFinetuneEngine\n\n"
        "train = generate_qa_embedding_pairs(nodes, llm=llm)            # 用文档自动造 (问题, 相关块) 对\n"
        "engine = SentenceTransformersFinetuneEngine(train, model_id=\"BAAI/bge-small-en\",\n"
        "                                            model_output_path=\"ft_model\")\n"
        "engine.finetune()\n"
        "ft_model = engine.get_finetuned_model()                        # 用它重建索引，再按 L19/L22 评估",
        caption=L("示例：用自家 QA 对微调一个开源 embedding；llama-index-finetuning 在 core 之外，代码仅作演示",
                  "Illustrative: fine-tune an open-source embedding on your own QA pairs; llama-index-finetuning is outside core, code is for demonstration only"),
    )
    + c.source_ref(
        "(integration) llama-index-finetuning", "SentenceTransformersFinetuneEngine",
        L("用自家 QA 对微调 embedding，提升领域召回。",
          "fine-tunes embeddings on your QA pairs to lift domain recall."),
    )
    + d.flow([
        ("docs", L("自家文档", "your docs")),
        ("pairs", L("造 QA 对", "build QA pairs"), L("自动+人工挑", "auto + curate")),
        ("ft", L("微调 embedding", "fine-tune")),
        ("rebuild", L("换模型重建索引", "rebuild index")),
        ("eval", L("评估提升", "evaluate gain"), L("承 L19/L22", "per L19/L22")),
    ], caption=L("微调闭环：造对 → 微调 → 重建 → 评估，用数字证明提升",
                 "fine-tune loop: pairs → train → rebuild → evaluate; prove the gain with numbers"))
    + c.section(
        L("④ 性价比：微调贵又易过拟合——先穷尽更便宜的手段",
          "④ Cost-effectiveness: fine-tuning is pricey and overfit-prone — exhaust the cheaper levers first"),
        L(
            "微调不该是<strong>第一反应</strong>，而是<strong>最后一招</strong>。它<strong>贵</strong>：要造数据、要 GPU 训练、"
            "要<strong>重建整个索引</strong>、还要长期维护一个<strong>自有的模型版本</strong>；它<strong>容易过拟合</strong>："
            "QA 对是机器造的、数量又有限，模型可能学到的是“这批问题的腔调”而非“领域语义”，在真实问题上<strong>反而变差"
            "</strong>。所以在动微调之前，<strong>先把这串更便宜、风险更低的手段穷尽</strong>：① <strong>调 chunking（L06）"
            "</strong>——块太大太小都稀释语义，先把切块切对；② <strong>加 metadata（L07）</strong>——把标题 / 章节 / 关键词喂给"
            "检索，常常立竿见影；③ <strong>上 hybrid + rerank（L21）</strong>——向量召回配上关键词（BM25）兜住术语的精确匹配，"
            "再用 reranker 精排，多数“召回不准”到这一步就解决了；④ <strong>换更强的基座 embedding（L08）</strong>——直接换一个"
            "更大 / 更贴领域的开源或商用 embedding，常比自己微调一个小模型<strong>更省事也更稳</strong>。<strong>把这四样都"
            "试过、并用 L19/L22 确认“检索仍是瓶颈、根因确实是领域语义错位”</strong>，再考虑微调——这时它才真正<strong>划算"
            "</strong>。",
            "Fine-tuning shouldn't be your <strong>first reflex</strong> but your <strong>last resort</strong>. It is "
            "<strong>expensive</strong>: you build data, train on a GPU, <strong>rebuild the whole index</strong>, and "
            "maintain a <strong>private model version</strong> long-term; and it <strong>overfits easily</strong>: the "
            "QA pairs are machine-made and limited, so the model may learn “the phrasing of this batch” rather than "
            "“domain semantics” and get <strong>worse</strong> on real questions. So before touching fine-tuning, "
            "<strong>exhaust this chain of cheaper, lower-risk levers</strong>: (1) <strong>tune chunking (L06)</strong> "
            "— chunks too big or small dilute meaning, so cut them right first; (2) <strong>add metadata (L07)</strong> "
            "— feed titles / sections / keywords to retrieval, often an instant win; (3) <strong>bring in hybrid + "
            "rerank (L21)</strong> — pair vector recall with keywords (BM25) to nail exact term matches, then a reranker "
            "to refine — most “imprecise recall” is solved by here; (4) <strong>switch to a stronger base embedding "
            "(L08)</strong> — swap in a bigger / more domain-fit open-source or commercial embedding, often <strong>"
            "easier and steadier</strong> than fine-tuning a small one yourself. <strong>Only after trying all four and "
            "using L19/L22 to confirm “retrieval is still the bottleneck and the root cause really is domain "
            "misalignment”</strong> should you consider fine-tuning — that's when it's genuinely <strong>worth it"
            "</strong>.",
        ),
    )
    + c.analogy(L(
        "通用 embedding 像一本<strong>通用词典</strong>：覆盖面广，但对你<strong>行业内部的术语、缩写、黑话</strong>常常"
        "<strong>词不达意</strong>——把意思相近的两个行话词条<strong>放到八竿子打不着的两页</strong>。微调就像<strong>给你的"
        "行业单独编一本“术语对照表”</strong>：把“<strong>同一个意思的不同叫法</strong>”<strong>并到一处</strong>，让相近的"
        "领域概念在向量空间里<strong>真正靠在一起</strong>。但编这本对照表<strong>费时费钱、还容易编偏</strong>，所以只有当"
        "<strong>通用词典实在不够用</strong>、且你确认问题<strong>就出在词义对不齐</strong>时，才值得动手编。",
        "A generic embedding is like a <strong>general dictionary</strong>: broad coverage, but for your <strong>"
        "industry's own terms, acronyms, and slang</strong> it often <strong>misses the meaning</strong> — placing two "
        "in-context synonyms <strong>pages apart</strong>. Fine-tuning is like <strong>compiling a “glossary of terms” "
        "just for your industry</strong>: <strong>merging the different names for the same thing</strong> so related "
        "domain concepts <strong>actually sit together</strong> in vector space. But compiling that glossary is "
        "<strong>slow, costly, and easy to get wrong</strong>, so it's worth doing only when the <strong>general "
        "dictionary truly falls short</strong> and you've confirmed the problem is <strong>misaligned word meanings"
        "</strong>.",
    ))
    + c.key_points([
        L("<strong>痛点在地基</strong>：通用 embedding 在专业领域<strong>语义错位</strong>（术语 / 缩写 / 黑话映射不准），"
          "相关块进不了 top-k；这是<strong>召回阶段</strong>的漏，rerank / 合成都<strong>救不回</strong>。",
          "<strong>The pain is in the foundation</strong>: generic embeddings <strong>misalign</strong> in a domain "
          "(jargon / acronyms / slang mapped imprecisely), so relevant chunks never enter the top-k — a "
          "<strong>recall-stage</strong> leak that rerank / synthesis <strong>can't recover</strong>."),
        L("<strong>思路是对比学习</strong>：用 <code>generate_qa_embedding_pairs</code> 让 LLM 从自家文档<strong>反向造 "
          "(问题, 相关块) 对</strong>当信号，<strong>正样本拉近、负样本推远</strong>，校准领域语义。",
          "<strong>The idea is contrastive learning</strong>: use <code>generate_qa_embedding_pairs</code> to have an "
          "LLM <strong>reverse-build (question, chunk) pairs</strong> from your docs as signal, <strong>pulling "
          "positives closer and pushing negatives apart</strong> to calibrate domain semantics."),
        L("<strong>流程是四步闭环</strong>：造对 → <code>SentenceTransformersFinetuneEngine.finetune()</code> → <strong>换"
          "模型重建索引</strong>（向量不可混用）→ 按 <strong>L19/L22</strong> 的纪律、用 <strong>L12</strong> 的检索指标"
          "（<code>RetrieverEvaluator</code> 算 hit-rate / MRR）并入 L22 回归集<strong>量化前后</strong>，别只看训练 loss。",
          "<strong>The flow is a four-step loop</strong>: build pairs → "
          "<code>SentenceTransformersFinetuneEngine.finetune()</code> → <strong>rebuild the index with the new "
          "model</strong> (vectors can't be mixed) → following <strong>L19/L22</strong>'s discipline, quantify "
          "before/after with <strong>L12</strong>'s retrieval metrics (<code>RetrieverEvaluator</code> for hit-rate / "
          "MRR) plus an L22 regression set — not just the training loss."),
        L("<strong>性价比要算清</strong>：微调<strong>贵又易过拟合</strong>，先穷尽更便宜的手段——chunking（L06）、metadata"
          "（L07）、hybrid + rerank（L21）、换更强基座（L08）——确认检索仍是瓶颈、根因是领域错位再微调。",
          "<strong>Weigh the cost</strong>: fine-tuning is <strong>pricey and overfit-prone</strong>, so exhaust the "
          "cheaper levers first — chunking (L06), metadata (L07), hybrid + rerank (L21), a stronger base (L08) — and "
          "fine-tune only after confirming retrieval is still the bottleneck and the cause is domain misalignment."),
        L("<strong>分清 core 边界</strong>：<code>generate_qa_embedding_pairs</code> / "
          "<code>SentenceTransformersFinetuneEngine</code> 都来自 <strong>llama-index-finetuning（core 之外的集成）"
          "</strong>，本课代码为示例；评估用的 hit-rate / MRR 与回归集才是贯穿全书的真功夫。",
          "<strong>Mind the core boundary</strong>: <code>generate_qa_embedding_pairs</code> / "
          "<code>SentenceTransformersFinetuneEngine</code> both come from <strong>llama-index-finetuning (an "
          "out-of-core integration)</strong> and the code here is illustrative; the real craft running through the "
          "book is the hit-rate / MRR evaluation and regression set."),
    ])
    + c.design_highlight(L(
        "这是全书<strong>最后一课</strong>，落点却和<strong>第一课</strong>遥相呼应：L01 我们就掂量过“<strong>RAG 还是微调"
        "</strong>”，结论是知识该<strong>外置成可检索的索引</strong>、而非焊进权重。今天微调的<strong>不是 LLM、而是 "
        "embedding</strong>——校准的是“<strong>领域语义 → 向量</strong>”这层<strong>检索地基</strong>，恰恰是为了让<strong>"
        "检索</strong>更准，和 L01 那条主线<strong>始终一致</strong>。整本书其实在反复讲<strong>同一个判断</strong>：<strong>"
        "先量化、找瓶颈，再对症下药，永远用数字说话</strong>——切块（L06）、元数据（L07）、混合检索 + 重排（L21）、更强基座"
        "（L08）都是<strong>更便宜的药</strong>，微调是<strong>最贵的那一味</strong>，只在前面都不够、且 L19/L22 证明“检索仍是"
        "瓶颈、根因是领域错位”时才开；<strong>用完还得再用 L19/L22 证明它真有效、没过拟合</strong>——<strong>开头量化、结尾"
        "量化</strong>，正是这套手艺的纪律。三十五课走下来，你已经把 RAG 从<strong>“能跑一次”</strong>搭成了一条<strong>可检索、"
        "可评估、可观测、可上线、还能持续校准</strong>的工程管线。最后这块拼图——微调 embedding——留下的是一件朴素的提醒："
        "<strong>最强的优化，往往不是再加一层花哨的新组件，而是把最底层的地基，对着你的领域，校准准。</strong>",
        "This is the book's <strong>final lesson</strong>, yet it lands in <strong>quiet echo of the first</strong>: "
        "back in L01 we weighed “<strong>RAG vs fine-tuning</strong>” and concluded that knowledge belongs in a "
        "<strong>searchable, external index</strong> rather than welded into weights. What we fine-tune today is "
        "<strong>not the LLM but the embedding</strong> — calibrating the “<strong>domain semantics → vector</strong>” "
        "layer that is retrieval's <strong>bedrock</strong>, precisely to make <strong>retrieval</strong> sharper, "
        "fully <strong>consistent</strong> with L01's through-line. The whole book has, in truth, repeated <strong>one "
        "judgment</strong>: <strong>quantify first, find the bottleneck, then treat the cause — always speak with "
        "numbers</strong>. Chunking (L06), metadata (L07), hybrid + rerank (L21), a stronger base model (L08) are the "
        "<strong>cheaper medicines</strong>; fine-tuning is the <strong>priciest dose</strong>, prescribed only when "
        "those fall short and L19/L22 prove “retrieval is still the bottleneck and the cause is domain misalignment”; "
        "and <strong>after using it you must again use L19/L22 to prove it truly helped and didn't overfit</strong> — "
        "<strong>quantify at the start, quantify at the end</strong> is the discipline of this craft. Thirty-five "
        "lessons on, you've grown RAG from <strong>“runs once”</strong> into an engineering pipeline that is "
        "<strong>searchable, evaluable, observable, shippable, and continuously recalibrated</strong>. This last piece "
        "— fine-tuning embeddings — leaves one plain reminder: <strong>the strongest optimization is often not bolting "
        "on another shiny component, but calibrating the deepest foundation to fit your domain.</strong>",
    ))
)
