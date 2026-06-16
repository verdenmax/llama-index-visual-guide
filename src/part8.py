"""Part 8 (agentic depth & shipping): lessons 32-35. Content filled task-by-task."""
import components as c
import diagrams as d
import i18n
from i18n import L


def _skeleton(stage, zh_topic, en_topic):
    return (
        c.pipeline(stage)
        + c.lead(L(f"本课讲 <strong>{zh_topic}</strong>（内容完善中）。",
                   f"This lesson covers <strong>{en_topic}</strong> (being written)."))
        + d.flow([("a", L("场景", "Scenario")), ("b", L("做法", "Approach")), ("c", L("权衡", "Trade-off"))],
                 caption=L("占位流程图", "placeholder flow"))
        + d.compare2((L("不做", "Without"), i18n.render(L("有什么问题", "what breaks"))),
                     (L("做了", "With"), i18n.render(L("解决什么", "what it fixes"))),
                     caption=L("占位对照", "placeholder compare"))
        + c.analogy(L("占位类比。", "Placeholder analogy."))
        + c.key_points([L("本课要点占位。", "Key-points placeholder.")])
    )


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
LESSON_33 = _skeleton("answer", "人在回路（HITL）", "human-in-the-loop")
LESSON_34 = _skeleton("answer", "把 RAG 上线成服务", "serving your RAG")
LESSON_35 = _skeleton("embed", "微调 embedding", "fine-tuning embeddings")
